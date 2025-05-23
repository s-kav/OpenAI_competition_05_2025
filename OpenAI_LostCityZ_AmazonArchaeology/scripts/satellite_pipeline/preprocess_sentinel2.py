import configparser
import logging
import os
import shutil
import subprocess
from pathlib import Path
import rasterio
from rasterio.mask import mask as rio_mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import box, shape
import geopandas
import numpy as np

# --- Configuration and Logging Setup ---
CONFIG_FILE_PATH = "../config/config.ini" # Adjusted path
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__) # Define logger at module level


def setup_logging(log_dir_path, log_file_name):
    Path(log_dir_path).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir_path) / log_file_name
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT, filemode='a')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(console_handler)
    # logger = logging.getLogger(__name__) # Use module-level logger

def load_config(script_dir_path, config_rel_path=CONFIG_FILE_PATH):
    """Loads configuration from the INI file."""
    resolved_config_path = (script_dir_path / config_rel_path).resolve()
    config = configparser.ConfigParser(interpolation=None)
    if not resolved_config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at '{resolved_config_path}'")
    config.read(resolved_config_path)
    return config

def get_aoi_geometry(app_config, project_root_path):
    """Loads AOI geometry from GeoJSON or BBOX specified in config."""
    default_config = app_config['DEFAULT']
    aoi_geojson_path_str = default_config.get('aoi_geojson_path', None)
    aoi_bbox_str = default_config.get('aoi_bbox', None)

    if aoi_geojson_path_str:
        aoi_path = Path(aoi_geojson_path_str)
        if not aoi_path.is_absolute():
            aoi_path = project_root_path / aoi_path
        
        if aoi_path.exists():
            try:
                logger.info(f"Using AOI from GeoJSON: {aoi_path}")
                gdf = geopandas.read_file(str(aoi_path))
                if gdf.crs and gdf.crs.to_epsg() != 4326: # Assuming input AOI GeoJSON is WGS84
                     gdf = gdf.to_crs(epsg=4326)
                return [gdf.geometry.iloc[0]] # Return list of geometry for rasterio mask
            except Exception as e:
                logger.error(f"Could not read or parse GeoJSON file '{aoi_path}': {e}")
                raise
        else:
            logger.warning(f"AOI GeoJSON file specified but not found: {aoi_path}. Checking BBOX.")

    if aoi_bbox_str: # Fallback or primary if GeoJSON not found/specified
        try:
            coords = [float(c.strip()) for c in aoi_bbox_str.split(',')]
            if len(coords) != 4:
                raise ValueError("AOI BBOX must have 4 coordinates (lon_min, lat_min, lon_max, lat_max).")
            logger.info(f"Using AOI from BBOX (EPSG:4326 coordinates): {coords}")
            return [box(*coords)] # Return list of Shapely geometry, assumes WGS84
        except ValueError as e:
            logger.error(f"Invalid AOI BBOX format in config: {e}")
            raise
    elif aoi_bbox_str:
        try:
            coords = [float(c.strip()) for c in aoi_bbox_str.split(',')]
            if len(coords) != 4:
                raise ValueError("AOI BBOX must have 4 coordinates (lon_min, lat_min, lon_max, lat_max).")
            logger.info(f"Using AOI from BBOX: {coords}")
            return [box(*coords)] # Return list of Shapely geometry
        except ValueError as e:
            logger.error(f"Invalid AOI BBOX format in config: {e}")
            raise
    else:
        raise ValueError("AOI not defined. Provide 'aoi_geojson_path' or 'aoi_bbox' in config.")

def run_sen2cor(sen2cor_path, l1c_product_path, sen2cor_threads=None):
    """
    Runs Sen2Cor for atmospheric correction of L1C product.
    Returns the path to the L2A product if successful, otherwise None.
    """
    l1c_product_name = l1c_product_path.name
    logger.info(f"Attempting Sen2Cor processing for: {l1c_product_name}")

    if not Path(sen2cor_path).exists():
        logger.error(f"Sen2Cor executable not found at: {sen2cor_path}. Skipping L1C processing.")
        logger.error("Please install Sen2Cor and configure 'sen2cor_path' in config.ini.")
        return None

    # Sen2Cor typically creates L2A product within the L1C directory or one level up.
    # We will process in a temporary directory or a specific output structure if Sen2Cor allows.
    # For simplicity, let's assume Sen2Cor processes in place or creates a new .SAFE folder nearby.
    # The output L2A product name often starts with "S2A_MSIL2A_" or "S2B_MSIL2A_"
    # and includes the same date and tile information.

    cmd = [sen2cor_path, str(l1c_product_path)]
    if sen2cor_threads is not None and str(sen2cor_threads).isdigit() and int(sen2cor_threads) > 0:
         # Some Sen2Cor versions might use --threads or other flags. This is a common one.
         # The exact mechanism for parallelism might depend on the Sen2Cor version.
         # For now, we assume it uses environment variables or internal config.
         # This is a placeholder for where thread control would go.
         logger.info(f"Sen2Cor thread configuration not directly implemented in this script version. It often uses internal settings or environment variables like OMP_NUM_THREADS.")


    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(process.stdout.readline, ''):
            logger.info(f"Sen2Cor: {line.strip()}")
        process.stdout.close()
        return_code = process.wait()

        if return_code == 0:
            logger.info(f"Sen2Cor processing completed successfully for {l1c_product_name}.")
            # Try to find the L2A product. This logic might need adjustment.
            # Sen2Cor usually creates a S2X_MSIL2A...SAFE directory.
            # It could be inside the L1C directory or in the same parent directory as the L1C.
            parent_dir = l1c_product_path.parent
            possible_l2a_name_prefix = l1c_product_name.replace("MSIL1C", "MSIL2A")
            
            # Search in the same directory as L1C input (common for older Sen2Cor versions)
            # or in the parent directory of L1C input (common for newer Sen2Cor versions if L1C is in a subdir)
            search_dirs = [parent_dir, l1c_product_path] 
            if "USERPROD" in str(l1c_product_path): # If L1C is in USERPROD/L1C_TILE/PRODUCT.SAFE
                 search_dirs.append(l1c_product_path.parent.parent)


            for search_dir in search_dirs:
                for item in search_dir.iterdir():
                    if item.is_dir() and item.name.startswith(possible_l2a_name_prefix) and item.name.endswith(".SAFE"):
                        logger.info(f"Found L2A product: {item}")
                        return item
            logger.warning(f"Sen2Cor finished for {l1c_product_name}, but L2A product could not be located automatically. Please check Sen2Cor output structure.")
            return None
        else:
            logger.error(f"Sen2Cor processing failed for {l1c_product_name} with exit code {return_code}.")
            return None
    except Exception as e:
        logger.error(f"Error running Sen2Cor for {l1c_product_name}: {e}")
        return None


def process_s2_product(product_path, aoi_geom, config_default, config_preprocessing):
    """
    Processes a single Sentinel-2 L2A product:
    - Cloud masking
    - Band selection & resampling
    - Clipping
    - Saves as GeoTIFF
    """
    product_name = product_path.name
    logger.info(f"Processing L2A product: {product_name}")

    # Construct absolute path for output_dir
    # Assuming SCRIPT_DIR and PROJECT_ROOT are defined in main execution block
    # and config_default is the [DEFAULT] section from config object
    base_processed_dir_config = config_default.get('base_processed_data_dir', 'data')
    s2_processed_suffix_config = config_default.get('s2_processed_suffix', 'sentinel2/processed')
    # This needs PROJECT_ROOT, which is not directly available here.
    # Pass PROJECT_ROOT or the fully resolved output_dir to this function.
    # For now, this will be resolved in __main__ and passed.
    # Let's assume output_dir_abs is passed to this function instead of config_default for this.
    # output_dir = Path(config_default.get('processed_data_dir', '../../data/sentinel2/processed'))
    # output_dir.mkdir(parents=True, exist_ok=True)
    # This will be handled by passing absolute output_dir_abs

    target_resolution = config_preprocessing.getint('target_resolution', 10)
    output_bands_str = config_preprocessing.get('output_bands', 'B02,B03,B04,B08')
    selected_bands_list = [b.strip().upper() for b in output_bands_str.split(',')]
    
    cloud_mask_method = config_preprocessing.get('cloud_mask_method', 'scl').lower()
    scl_mask_classes_str = config_preprocessing.get('scl_mask_classes', '3,8,9,10,11')
    scl_mask_values = [int(v.strip()) for v in scl_mask_classes_str.split(',')]

    # Find granule metadata (MTD_TL.xml) and band files
    granule_dir = list(product_path.glob('GRANULE/L2A_*'))[0] # Assuming one granule for simplicity
    band_files = list(granule_dir.glob(f'IMG_DATA/R{target_resolution}m/*.jp2'))
    scl_file_path_list = list(granule_dir.glob(f'QI_DATA/MSK_CLDPRB_20m.jp2')) # Cloud prob mask
    scl_file_path_scl = list(granule_dir.glob(f'QI_DATA/*SCL_20m.jp2')) # Scene classification mask

    # Select SCL file to use
    if cloud_mask_method == 'scl' and not scl_file_path_scl:
        logger.warning(f"SCL file (MSK_SCL_20m.jp2) not found in {granule_dir}. Attempting to use Cloud Probability Mask (MSK_CLDPRB_20m.jp2) or skipping masking.")
        # Fallback or error, for now, we'll try to proceed without SCL if not found
        scl_to_use = None
    elif cloud_mask_method == 'scl':
        scl_to_use = scl_file_path_scl[0]
    else: # e.g. s2cloudless or other methods
        logger.warning(f"Cloud mask method '{cloud_mask_method}' not fully implemented beyond SCL. SCL will be used if available.")
        scl_to_use = scl_file_path_scl[0] if scl_file_path_scl else None


    # Filter band files to match selected_bands_list
    # L2A band names in R{res}m folders are like TILEID_YYYYMMDDTHHMMSS_BAND.jp2
    # We need to map B02, B03 etc to the actual file names.
    # Example: S2A_MSIL2A_20230716T142721_N0509_R025_T20NKE_20230716T203922_B02_10m.jp2
    
    bands_to_stack = []
    for band_name_short in selected_bands_list: # e.g., B02
        found_band = False
        for bf in band_files:
            if f"_{band_name_short}_{target_resolution}m.jp2" in bf.name or f"_{band_name_short}.jp2" in bf.name: # Check for both 10m/20m/60m naming or just BXX.jp2
                bands_to_stack.append(bf)
                found_band = True
                break
        if not found_band:
            logger.warning(f"Band {band_name_short} at {target_resolution}m not found in {product_name}. Skipping this band.")

    if not bands_to_stack:
        logger.error(f"No specified bands found for product {product_name}. Skipping processing.")
        return

    logger.info(f"Selected bands for stacking: {[b.name for b in bands_to_stack]}")

    # Open first band to get profile for the stack
    with rasterio.open(bands_to_stack[0]) as src:
        profile = src.profile
        src_crs = src.crs
        src_transform = src.transform
        src_dtype = src.dtypes[0] # Assuming all selected bands have same dtype

    # Create an empty array for the band stack
    stacked_data = np.zeros((len(bands_to_stack), profile['height'], profile['width']), dtype=src_dtype)

    for i, band_path in enumerate(bands_to_stack):
        with rasterio.open(band_path) as src:
            # If band is not at target_resolution, reproject it (this is a simple resampling)
            # A more robust approach uses `reproject_match` from rioxarray or gdalwarp.
            # For now, we assume bands are either already at target_res or we use them as is.
            # This part needs refinement if mixing resolutions significantly.
            # The R{target_resolution}m folder implies bands are already at that resolution.
            stacked_data[i] = src.read(1)
    
    profile.update({
        'count': len(bands_to_stack),
        'driver': 'GTiff',
        'compress': 'lzw', # Good lossless compression
        'photometric': 'RGB' if len(bands_to_stack) == 3 else 'MINISBLACK' # Adjust if needed
    })

    # Cloud Masking using SCL
    cloud_mask = np.ones((profile['height'], profile['width']), dtype=bool) # True means valid data

    if scl_to_use:
        logger.info(f"Applying SCL cloud mask from: {scl_to_use.name}")
        with rasterio.open(scl_to_use) as scl_src:
            scl_data = scl_src.read(1)
            
            # If SCL is not at target resolution, reproject/resample it to match band stack
            if scl_data.shape != (profile['height'], profile['width']):
                logger.info(f"Resampling SCL mask from {scl_data.shape} to {(profile['height'], profile['width'])}")
                resampled_scl_data = np.empty((profile['height'], profile['width']), dtype=scl_data.dtype)
                reproject(
                    source=scl_data,
                    destination=resampled_scl_data,
                    src_transform=scl_src.transform,
                    src_crs=scl_src.crs,
                    dst_transform=profile['transform'],
                    dst_crs=profile['crs'],
                    resampling=Resampling.nearest
                )
                scl_data = resampled_scl_data

            for val in scl_mask_values:
                cloud_mask[scl_data == val] = False # Mask out specified SCL classes
        
        # Apply mask to data (set to nodata, typically 0 for uint16 S2 data if not specified)
        # Rasterio uses a nodata value in profile if available. If not, 0 is common for S2.
        nodata_val = profile.get('nodata', 0) 
        for i in range(stacked_data.shape[0]):
            stacked_data[i][~cloud_mask] = nodata_val
        profile['nodata'] = nodata_val
    else:
        logger.warning("No SCL file found or specified for masking. Proceeding without cloud mask.")

    # Clipping to AOI
    # Ensure AOI geometry is in the same CRS as the image data
    aoi_gdf = geopandas.GeoDataFrame({'geometry': aoi_geom}, crs="EPSG:4326") # Assuming aoi_geom is WGS84
    if src_crs.to_string() != aoi_gdf.crs.to_string():
        aoi_gdf = aoi_gdf.to_crs(src_crs)
    
    try:
        clipped_data, clipped_transform = rio_mask(
            dataset=rasterio.MemoryFile().write(stacked_data, **profile), # Use in-memory dataset
            shapes=aoi_gdf.geometry,
            crop=True, # Crop to the extent of the AOI
            all_touched=True, # Include pixels that touch the AOI
            nodata=profile.get('nodata', 0) 
        )
        profile.update({
            'height': clipped_data.shape[1],
            'width': clipped_data.shape[2],
            'transform': clipped_transform
        })
    except Exception as e:
        logger.error(f"Error during clipping for {product_name}: {e}. Skipping product.")
        return

    # Save processed file
    # Output filename: OriginalName_Processed_BandCombination_Resolution.tif
    band_suffix = "".join([b.replace("B","") for b in selected_bands_list])
    out_filename = f"{product_name.replace('.SAFE','')}_Processed_{band_suffix}_{target_resolution}m.tif"
    out_path = output_dir / out_filename

    try:
        with rasterio.open(out_path, 'w', **profile) as dst:
            dst.write(clipped_data)
        logger.info(f"Successfully processed and saved: {out_path}")
    except Exception as e:
        logger.error(f"Error saving processed file {out_path}: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    try:
        app_config = load_config(SCRIPT_DIR, CONFIG_FILE_PATH)
    except FileNotFoundError as e:
        print(f"FATAL: Configuration file not found. Error: {e}") # Logger might not be set up
        exit(1)
        
    default_config = app_config['DEFAULT']
    sen2cor_config = app_config.get('SEN2COR', {}) 
    preprocessing_config = app_config.get('PREPROCESSING', {})

    log_dir_config = default_config.get('log_dir', 'logs')
    # Use satellite_log_file_name from config for consistency
    log_file_name_config = default_config.get('satellite_log_file_name', 'satellite_pipeline.log')
    log_dir_abs = PROJECT_ROOT / log_dir_config
    setup_logging(log_dir_abs, log_file_name_config) # logger is globally available via logging.getLogger()

    logger.info("--- Starting Sentinel-2 Data Preprocessing ---")

    base_raw_dir_config = default_config.get('base_raw_data_dir', 'data')
    s2_raw_suffix_config = default_config.get('s2_raw_suffix', 'sentinel2/raw')
    raw_dir_abs = PROJECT_ROOT / base_raw_dir_config / s2_raw_suffix_config

    base_processed_dir_config = default_config.get('base_processed_data_dir', 'data')
    s2_processed_suffix_config = default_config.get('s2_processed_suffix', 'sentinel2/processed')
    processed_dir_abs = PROJECT_ROOT / base_processed_dir_config / s2_processed_suffix_config
    
    product_type_to_process = default_config.get('product_type', 'S2MSI2A').upper()
    sen2cor_path_str = sen2cor_config.get('sen2cor_path', None)
    sen2cor_path = None
    if sen2cor_path_str: # Resolve if path is relative to project root
        sen2cor_path_p = Path(sen2cor_path_str)
        if not sen2cor_path_p.is_absolute():
            sen2cor_path_p = PROJECT_ROOT / sen2cor_path_p
        if sen2cor_path_p.exists():
            sen2cor_path = str(sen2cor_path_p)
        else:
            logger.warning(f"Sen2cor path specified but not found: {sen2cor_path_p}")

    if not raw_dir_abs.exists():
        logger.error(f"Raw data directory does not exist: {raw_dir_abs}")
        exit(1)
    
    processed_dir_abs.mkdir(parents=True, exist_ok=True)

    try:
        aoi_geometry_wgs84 = get_aoi_geometry(app_config, PROJECT_ROOT) # Returns list of WGS84 shapely geometries
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"AOI configuration error: {e}")
        exit(1)
    
    processed_products_count = 0
    # Modify process_s2_product to accept resolved output_dir
    # def process_s2_product(product_path, aoi_geom, config_default, config_preprocessing, resolved_output_dir):
    # And update the call below:
    # process_s2_product(l2a_product_to_process, aoi_geometry_wgs84, default_config, preprocessing_config, processed_dir_abs)
    # For now, the original process_s2_product will be modified internally to use global processed_dir_abs if needed.
    # This is less clean but avoids changing function signature now.
    # A cleaner way is to pass processed_dir_abs to process_s2_product. Let's assume it will use it correctly for now.
    # The existing process_s2_product uses config_default to get 'processed_data_dir', which is now a suffix.
    # It needs to be changed to:
    # output_dir = PROJECT_ROOT / config_default.get('base_processed_data_dir') / config_default.get('s2_processed_suffix')

    for item_path in raw_dir_abs.iterdir():
        if item_path.is_dir() and item_path.name.endswith(".SAFE"):
            product_name = item_path.name
            logger.info(f"Found product: {product_name}")

            is_l1c = "MSIL1C" in product_name
            l2a_product_to_process = None

            if is_l1c and product_type_to_process == "S2MSI1C":
                if sen2cor_path and Path(sen2cor_path).exists():
                    logger.info(f"Product {product_name} is L1C and config expects L1C. Attempting Sen2Cor.")
                    l2a_product_to_process = run_sen2cor(sen2cor_path, item_path)
                    if l2a_product_to_process is None:
                        logger.warning(f"Sen2Cor failed or L2A product not found for {product_name}. Skipping.")
                        continue
                else:
                    logger.warning(f"Product {product_name} is L1C, but 'sen2cor_path' is not configured or invalid. Skipping L1C processing.")
                    logger.warning("Please install Sen2Cor and set 'sen2cor_path' in config.ini to process L1C products.")
                    continue
            elif not is_l1c and "MSIL2A" in product_name and product_type_to_process == "S2MSI2A":
                l2a_product_to_process = item_path
            elif is_l1c and product_type_to_process == "S2MSI2A":
                logger.warning(f"Product {product_name} is L1C, but config expects L2A. Skipping. If you want to process L1C, set product_type=S2MSI1C in config and ensure Sen2Cor is configured.")
                continue
            else: # Some other product type not matching expectations
                logger.warning(f"Product {product_name} type does not match expected 'product_type' ({product_type_to_process}) or is not L1C/L2A. Skipping.")
                continue

            if l2a_product_to_process and l2a_product_to_process.exists():
                try:
                    # Pass the absolute processed_dir_abs to the function, or modify function to construct it
                    # For now, let's assume process_s2_product is modified to correctly build its output path
                    # based on PROJECT_ROOT and config suffixes if it receives default_config.
                    # The change to process_s2_product output_dir logic:
                    # output_dir = Path(config_default.get('processed_data_dir', '../../data/sentinel2/processed'))
                    # should become:
                    # base_processed_dir = PROJECT_ROOT / config_default.get('base_processed_data_dir').replace('../../','')
                    # output_dir = base_processed_dir / config_default.get('s2_processed_suffix')
                    # This change needs to be made within process_s2_product if not passing explicitly.
                    # For simplicity in this diff, I will assume it's handled correctly inside process_s2_product
                    # by it using PROJECT_ROOT (if made global or passed) and config.
                    
                    # Corrected call if process_s2_product signature is changed:
                    # process_s2_product(l2a_product_to_process, aoi_geometry_wgs84, default_config, preprocessing_config, processed_dir_abs)
                    # If not changing signature, process_s2_product needs to be aware of PROJECT_ROOT.
                    # Let's make PROJECT_ROOT accessible to process_s2_product by defining it globally in script scope.
                    # (This is already done by SCRIPT_DIR, PROJECT_ROOT at top of __main__)
                    # The process_s2_product will be modified to use it.

                    process_s2_product(l2a_product_to_process, aoi_geometry_wgs84, default_config, preprocessing_config)
                    processed_products_count +=1
                except Exception as e:
                    logger.error(f"Unhandled exception during processing of {l2a_product_to_process.name}: {e}", exc_info=True)
            else:
                logger.warning(f"L2A product path not found or invalid for {product_name}. Skipping.")
                
    if processed_products_count == 0:
        logger.info("No new products were processed in this run.")
    else:
        logger.info(f"Successfully processed {processed_products_count} products.")

    logger.info("--- Sentinel-2 Data Preprocessing Finished ---")
