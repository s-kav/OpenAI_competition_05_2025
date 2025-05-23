import configparser
import logging
import os
import json
import pdal
import rasterio
from rasterio.mask import mask as rio_mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio import Affine
from shapely.geometry import box
import geopandas
import numpy as np
from pathlib import Path
import laspy # For LAZ to LAS conversion if chosen


# --- Configuration and Logging Setup ---
CONFIG_FILE_PATH = "../config/config.ini" # Adjusted path
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__) # Define logger at module level


def setup_logging(log_dir_path, log_file_name):
    Path(log_dir_path).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir_path) / log_file_name
    logger_root = logging.getLogger()
    if logger_root.hasHandlers(): # Clear existing handlers
        for handler in logger_root.handlers[:]:
            logger_root.removeHandler(handler)
    logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT, filemode='a')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(console_handler) # Add console handler to root logger
    # logger = logging.getLogger(__name__) # Use module-level logger

def load_config(script_dir_path, config_rel_path=CONFIG_FILE_PATH):
    """Loads configuration from the INI file."""
    resolved_config_path = (script_dir_path / config_rel_path).resolve()
    config = configparser.ConfigParser(interpolation=None)
    if not resolved_config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at '{resolved_config_path}'")
    config.read(resolved_config_path)
    return config

def get_aoi_geometry_from_config(app_config_default, project_root_path):
    """Loads AOI geometry from GeoJSON or BBOX specified in config's DEFAULT section."""
    aoi_geojson_path_str = app_config_default.get('aoi_geojson_path', None)
    aoi_bbox_str = app_config_default.get('aoi_bbox', None)

    if aoi_geojson_path_str:
        aoi_path = Path(aoi_geojson_path_str)
        if not aoi_path.is_absolute():
            aoi_path = project_root_path / aoi_path # Resolve from project root
        
        if aoi_path.exists():
            try:
                logger.info(f"Using AOI from GeoJSON: {aoi_path}")
                gdf = geopandas.read_file(str(aoi_path))
                if gdf.crs and gdf.crs.to_epsg() != 4326: # Assuming input AOI GeoJSON is WGS84
                     gdf = gdf.to_crs(epsg=4326)
                return [gdf.geometry.iloc[0]] # Return list of Shapely geometries
            except Exception as e:
                logger.error(f"Could not read or parse GeoJSON file '{aoi_path}': {e}")
                raise
        else:
            logger.warning(f"AOI GeoJSON file specified but not found: {aoi_path}. Checking BBOX.")

    if aoi_bbox_str: # Fallback or primary
        try:
            coords = [float(c.strip()) for c in aoi_bbox_str.split(',')]
            if len(coords) != 4:
                raise ValueError("AOI BBOX must have 4 coordinates (lon_min, lat_min, lon_max, lat_max).")
            logger.info(f"Using AOI from BBOX (EPSG:4326 coordinates): {coords}")
            return [box(*coords)] # Returns a list with one Shapely geometry, assumes WGS84
        except ValueError as e:
            logger.error(f"Invalid AOI BBOX format in config: {e}")
            raise
    elif aoi_bbox_str:
        try:
            coords = [float(c.strip()) for c in aoi_bbox_str.split(',')]
            if len(coords) != 4:
                raise ValueError("AOI BBOX must have 4 coordinates (lon_min, lat_min, lon_max, lat_max).")
            logger.info(f"Using AOI from BBOX (EPSG:4326): {coords}")
            return [box(*coords)] # Returns a list with one Shapely geometry
        except ValueError as e:
            logger.error(f"Invalid AOI BBOX format in config: {e}")
            raise
    else:
        raise ValueError("AOI not defined. Provide 'aoi_geojson_path' or 'aoi_bbox' in DEFAULT config.")

def convert_laz_to_las(laz_filepath, las_filepath):
    """Converts a LAZ file to LAS using laspy."""
    try:
        logger.info(f"Converting {laz_filepath.name} to LAS format...")
        laz = laspy.read(laz_filepath)
        las = laspy.create(point_format=laz.header.point_format, file_version=laz.header.version)
        las.points = laz.points
        las.write(las_filepath)
        logger.info(f"Successfully converted to {las_filepath.name}")
        return True
    except Exception as e:
        logger.error(f"Error converting LAZ to LAS for {laz_filepath.name}: {e}")
        return False

def run_pdal_pipeline(input_file, output_file, pipeline_json_template_str, replacements):
    """Runs a PDAL pipeline after replacing placeholders in the JSON string."""
    try:
        pipeline_json_str = pipeline_json_template_str
        for placeholder, value in replacements.items():
            pipeline_json_str = pipeline_json_str.replace(placeholder, str(value))
        
        pipeline_json = json.loads(pipeline_json_str) # Validate JSON
        # Ensure filenames in pipeline are absolute paths for PDAL
        for stage in pipeline_json.get("pipeline", []):
            if "filename" in stage:
                 if stage["filename"] == "INPUT_FILE_PLACEHOLDER_RESOLVED": # Special case for primary input
                     stage["filename"] = str(Path(input_file).resolve())
                 elif stage["filename"] == "OUTPUT_FILE_PLACEHOLDER_RESOLVED": # Special case for primary output
                     stage["filename"] = str(Path(output_file).resolve())
                 # Other filenames in pipeline could be made absolute if needed
        
        logger.info(f"Executing PDAL pipeline for output: {Path(output_file).name}")
        # logger.debug(f"PDAL Pipeline JSON: {json.dumps(pipeline_json, indent=2)}") # Can be very verbose

        pipeline = pdal.Pipeline(json.dumps(pipeline_json))
        pipeline.execute()
        
        if pipeline.rating > 0: # PDAL rating can indicate issues
             logger.warning(f"PDAL pipeline for {Path(output_file).name} completed with rating {pipeline.rating}. Check logs if issues.")
        else:
            logger.info(f"PDAL pipeline for {Path(output_file).name} completed successfully.")
        return True
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in PDAL pipeline template: {e}")
        logger.error(f"Problematic JSON string snippet: {pipeline_json_str[:500]}") # Log part of the string
        return False
    except RuntimeError as e: # PDAL execution errors
        logger.error(f"PDAL runtime error for {Path(output_file).name}: {e}")
        # logger.error(f"PDAL Pipeline that failed: {json.dumps(pipeline_json, indent=2)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error running PDAL pipeline for {Path(output_file).name}: {e}")
        # logger.error(f"PDAL Pipeline that failed: {json.dumps(pipeline_json, indent=2)}")
        return False

def generate_hillshade(dtm_path, hillshade_path, azimuth=315, altitude=45, z_factor=1, multi_directional=False):
    """Generates a hillshade raster from a DTM using Rasterio (GDAL)."""
    try:
        logger.info(f"Generating hillshade for {dtm_path.name} -> {hillshade_path.name}")
        with rasterio.open(dtm_path) as src_ds:
            profile = src_ds.profile.copy()
            profile.update(dtype=rasterio.uint8, count=1, compress='lzw', nodata=0) # Hillshade is typically 8-bit

            if multi_directional:
                logger.info("Generating multi-directional hillshade.")
                azimuths = [315, 270, 225, 180] # Example directions
                altitude_val = altitude
                hillshade_sum = np.zeros(src_ds.shape, dtype=np.float32)
                
                for i, az in enumerate(azimuths):
                    temp_hillshade_path = hillshade_path.with_name(f"{hillshade_path.stem}_temp_{az}.tif")
                    subprocess.run([
                        "gdaldem", "hillshade",
                        "-az", str(az),
                        "-alt", str(altitude_val),
                        "-z", str(z_factor),
                        "-of", "GTiff",
                        str(dtm_path),
                        str(temp_hillshade_path)
                    ], check=True, capture_output=True, text=True)
                    with rasterio.open(temp_hillshade_path) as temp_hs_ds:
                        hillshade_sum += temp_hs_ds.read(1)
                    temp_hillshade_path.unlink() # Clean up temp file
                
                hillshade_data = (hillshade_sum / len(azimuths)).astype(rasterio.uint8)

            else: # Single direction
                temp_hillshade_path = hillshade_path.with_name(f"{hillshade_path.stem}_temp.tif")
                # Using gdaldem via subprocess as rasterio.fill.main.hillshade is not directly exposed
                # and `gdal.DEMProcessing` through Python bindings can be cumbersome for simple cases.
                result = subprocess.run([
                    "gdaldem", "hillshade",
                    "-az", str(azimuth),
                    "-alt", str(altitude),
                    "-z", str(z_factor),
                    "-of", "GTiff", # Output format
                    str(dtm_path), # Input DTM
                    str(temp_hillshade_path) # Output hillshade
                ], check=True, capture_output=True, text=True) # Capture output for logging
                
                if result.stderr:
                    logger.info(f"GDAL Hillshade STDERR: {result.stderr}")

                with rasterio.open(temp_hillshade_path) as temp_hs_ds:
                    hillshade_data = temp_hs_ds.read(1) # Read the single band
                temp_hillshade_path.unlink() # Clean up temp file

            with rasterio.open(hillshade_path, 'w', **profile) as dst_ds:
                dst_ds.write(hillshade_data, 1)
            
            logger.info(f"Successfully generated hillshade: {hillshade_path.name}")
            return True

    except subprocess.CalledProcessError as e:
        logger.error(f"GDAL Hillshade command failed for {dtm_path.name}: {e}")
        logger.error(f"GDAL STDERR: {e.stderr}")
        logger.error(f"GDAL STDOUT: {e.stdout}")
        return False
    except Exception as e:
        logger.error(f"Error generating hillshade for {dtm_path.name}: {e}")
        return False

def clip_raster(input_raster_path, output_raster_path, aoi_geometries, target_crs_epsg):
    """Clips a raster to the AOI geometries."""
    try:
        logger.info(f"Clipping {input_raster_path.name} to AOI -> {output_raster_path.name}")
        with rasterio.open(input_raster_path) as src:
            # Ensure AOI is in the same CRS as the raster
            aoi_gdf = geopandas.GeoDataFrame({'geometry': aoi_geometries}, crs="EPSG:4326") # Assuming AOI is WGS84
            if src.crs and src.crs.to_string().upper() != aoi_gdf.crs.to_string().upper(): # Check if src.crs is not None
                logger.info(f"Reprojecting AOI from {aoi_gdf.crs} to {src.crs} for clipping.")
                aoi_gdf = aoi_gdf.to_crs(src.crs)
            
            shapes_for_mask = list(aoi_gdf.geometry)

            out_image, out_transform = rio_mask(src, shapes_for_mask, crop=True, all_touched=True)
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
                "crs": src.crs # CRS should be preserved from source
            })

            with rasterio.open(output_raster_path, "w", **out_meta) as dest:
                dest.write(out_image)
            logger.info(f"Successfully clipped raster to {output_raster_path.name}")
            return True
    except Exception as e:
        logger.error(f"Error clipping raster {input_raster_path.name}: {e}", exc_info=True)
        return False

# --- Main Execution ---
if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    try:
        app_config = load_config(SCRIPT_DIR, CONFIG_FILE_PATH)
    except FileNotFoundError as e:
        print(f"FATAL: Configuration file not found. Error: {e}") # Logger not set up
        exit(1)

    default_config = app_config['DEFAULT']
    lidar_config = app_config.get('LIDAR')

    if not lidar_config:
        print("FATAL: [LIDAR] section not found in configuration file.") # Logger not set up
        exit(1)

    log_dir_config = default_config.get('log_dir', 'logs')
    log_file_name_config = lidar_config.get('lidar_log_file_name', default_config.get('lidar_log_file_name','lidar_pipeline.log'))
    log_dir_abs = PROJECT_ROOT / log_dir_config
    setup_logging(log_dir_abs, log_file_name_config) # logger is globally available

    logger.info("--- Starting LiDAR Data Preprocessing ---")

    base_raw_dir_config = default_config.get('base_raw_data_dir', 'data')
    lidar_raw_suffix_config = lidar_config.get('lidar_raw_suffix', 'lidar/raw')
    raw_lidar_dir_abs = PROJECT_ROOT / base_raw_dir_config / lidar_raw_suffix_config

    base_processed_dir_config = default_config.get('base_processed_data_dir', 'data')
    lidar_processed_suffix_config = lidar_config.get('lidar_processed_suffix', 'lidar/processed')
    processed_lidar_dir_abs = PROJECT_ROOT / base_processed_dir_config / lidar_processed_suffix_config
    
    Path(processed_lidar_dir_abs).mkdir(parents=True, exist_ok=True)
    logger.info(f"Raw LiDAR data source: {raw_lidar_dir_abs}")
    logger.info(f"Processed LiDAR data will be saved to: {processed_lidar_dir_abs}")

    # Load AOI
    try:
        aoi_geom_list_wgs84 = get_aoi_geometry_from_config(default_config, PROJECT_ROOT) # Expects list of WGS84 geometries
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"AOI configuration error: {e}. Exiting.")
        exit(1)

    # PDAL and processing parameters
    target_projected_crs = lidar_config.get('target_projected_crs', None)
    if not target_projected_crs or not target_projected_crs.startswith("EPSG:"):
        logger.error("CRITICAL: 'target_projected_crs' (e.g., EPSG:31980) must be defined in [LIDAR] config for PDAL processing. Exiting.")
        exit(1)

    gnd_pipeline_template = lidar_config.get('ground_classification_pipeline_json')
    dtm_pipeline_template = lidar_config.get('dtm_generation_pipeline_json')
    dtm_resolution = lidar_config.getfloat('dtm_resolution', 1.0)
    dtm_interp_method = lidar_config.get('dtm_interpolation_method', 'mean')
    
    hs_azimuth = lidar_config.getint('hillshade_azimuth', 315)
    hs_altitude = lidar_config.getint('hillshade_altitude', 45)
    hs_z_factor = lidar_config.getfloat('hillshade_z_factor', 1.0)
    hs_multi = lidar_config.getboolean('multi_directional_hillshade', True)

    processed_files_count = 0
    for raw_file_path in raw_lidar_dir.iterdir():
        if not (raw_file_path.name.lower().endswith(".laz") or raw_file_path.name.lower().endswith(".las")):
            continue

        logger.info(f"Processing file: {raw_file_path.name}")
        base_name = raw_file_path.stem
        
        # Determine input for PDAL (either original .las or converted .las)
        input_for_pdal = raw_file_path
        if raw_file_path.name.lower().endswith(".laz"):
            converted_las_path = processed_lidar_dir / f"{base_name}_converted.las"
            if not converted_las_path.exists(): # Avoid re-conversion
                if not convert_laz_to_las(raw_file_path, converted_las_path):
                    logger.error(f"Skipping {raw_file_path.name} due to LAZ conversion error.")
                    continue
            input_for_pdal = converted_las_path
        
        # --- Ground Classification ---
        ground_points_las = processed_lidar_dir / f"{base_name}_ground.las"
        if not ground_points_las.exists(): # Avoid re-processing
            gnd_replacements = {
                "INPUT_FILE_PLACEHOLDER": str(input_for_pdal.resolve()), # For PDAL, ensure paths are absolute
                "OUTPUT_GROUND_FILE_PLACEHOLDER": str(ground_points_las.resolve()),
                "TARGET_PROJECTED_CRS_PLACEHOLDER": target_projected_crs
            }
            if not run_pdal_pipeline(str(input_for_pdal.resolve()), str(ground_points_las.resolve()), gnd_pipeline_template, gnd_replacements):
                logger.error(f"Skipping DTM/hillshade for {raw_file_path.name} due to ground classification error.")
                continue
        else:
            logger.info(f"Ground classified file {ground_points_las.name} already exists. Using it.")

        # --- DTM Generation ---
        dtm_unclipped_path = processed_lidar_dir / f"{base_name}_dtm_unclipped.tif"
        if not dtm_unclipped_path.exists(): # Avoid re-processing
            dtm_replacements = {
                "INPUT_GROUND_POINTS_PLACEHOLDER": str(ground_points_las.resolve()),
                "OUTPUT_DTM_FILE_PLACEHOLDER": str(dtm_unclipped_path.resolve()),
                "DTM_RESOLUTION_PLACEHOLDER": dtm_resolution,
                "DTM_INTERPOLATION_METHOD_PLACEHOLDER": dtm_interp_method,
                "TARGET_PROJECTED_CRS_PLACEHOLDER": target_projected_crs
            }
            if not run_pdal_pipeline(str(ground_points_las.resolve()), str(dtm_unclipped_path.resolve()), dtm_pipeline_template, dtm_replacements):
                logger.error(f"Skipping hillshade for {raw_file_path.name} due to DTM generation error.")
                continue
        else:
            logger.info(f"Unclipped DTM {dtm_unclipped_path.name} already exists. Using it.")
        
        # --- Clipping DTM ---
        dtm_clipped_path = processed_lidar_dir / f"{base_name}_dtm_clipped_aoi.tif"
        # Use target_projected_crs for clipping as DTM is in this CRS
        if not clip_raster(dtm_unclipped_path, dtm_clipped_path, aoi_geom_list_wgs84, target_projected_crs):
            logger.error(f"Failed to clip DTM for {raw_file_path.name}. Hillshade will use unclipped DTM.")
            # Use unclipped DTM for hillshade if clipping fails
            dtm_for_hillshade = dtm_unclipped_path 
        else:
            dtm_for_hillshade = dtm_clipped_path


        # --- Hillshade Generation (from potentially clipped DTM) ---
        hillshade_unclipped_path = processed_lidar_dir / f"{base_name}_hillshade_unclipped.tif" # if dtm_for_hillshade is unclipped
        hillshade_clipped_path = processed_lidar_dir / f"{base_name}_hillshade_clipped_aoi.tif" # if dtm_for_hillshade is clipped
        
        target_hillshade_path = hillshade_clipped_path if dtm_for_hillshade == dtm_clipped_path else hillshade_unclipped_path

        if not generate_hillshade(dtm_for_hillshade, target_hillshade_path, hs_azimuth, hs_altitude, hs_z_factor, hs_multi):
             logger.warning(f"Failed to generate hillshade for {dtm_for_hillshade.name}")
        
        processed_files_count +=1
        logger.info(f"Finished processing stages for: {raw_file_path.name}")

    if processed_files_count == 0:
        logger.info("No new LiDAR files were processed in this run (either no raw files or all outputs exist).")
    else:
        logger.info(f"Successfully processed or verified outputs for {processed_files_count} LiDAR files.")
    logger.info("--- LiDAR Data Preprocessing Finished ---")
