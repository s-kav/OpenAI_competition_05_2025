import configparser
import logging
import os
from datetime import datetime
from pathlib import Path

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, SentinelsatAPIError

# --- Configuration and Logging Setup ---
# Assuming this script is in OpenAI_LostCityZ_AmazonArchaeology/scripts/satellite_pipeline/
# And config.ini is in OpenAI_LostCityZ_AmazonArchaeology/config/
CONFIG_FILE_PATH = "../config/config.ini"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__) # Define logger at module level

def setup_logging(log_dir_path, log_file_name):
    """Sets up logging configuration."""
    Path(log_dir_path).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir_path) / log_file_name
    
    # Clear existing handlers for the root logger to avoid duplicate logs
    # if this function is called multiple times or in a testing environment.
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            
    logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT, filemode='a')
    # Also print logs to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(console_handler)
    # logger = logging.getLogger(__name__) # Use module-level logger

def load_config(script_dir_path, config_rel_path=CONFIG_FILE_PATH):
    """
    Loads configuration from the INI file.
    The config_rel_path is expected to be relative to the script_dir_path's parent (i.e., scripts/ directory).
    """
    # config_file should be relative to the project root, e.g. "config/config.ini"
    # If script_dir_path = /path/to/project/scripts/pipeline_type
    # then script_dir_path.parent.parent = /path/to/project
    # config_path = script_dir_path.parent.parent / "config" / "config.ini"
    
    # The CONFIG_FILE_PATH = "../config/config.ini" means it's one level up from script_dir, then into config.
    # So, if script_dir is scripts/satellite_pipeline/, then ../ goes to scripts/, then config/config.ini
    # This means config_path should be: script_dir.parent / "config" / "config.ini"
    # Let's adjust CONFIG_FILE_PATH to be relative from project root perspective
    # For scripts, config is at PROJECT_ROOT / "config" / "config.ini"
    # If CONFIG_FILE_PATH is "../config/config.ini", it resolves from script_dir.
    
    # Correct resolution: CONFIG_FILE_PATH is already "correct" relative to script location.
    # Path(__file__).parent / "../config/config.ini"
    resolved_config_path = (script_dir_path / config_rel_path).resolve()

    config = configparser.ConfigParser(interpolation=None) # Allow paths with %
    if not resolved_config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at '{resolved_config_path}'")

    config.read(resolved_config_path)
    # Return the whole config object to access different sections
    return config

# --- Main Acquisition Logic ---
def get_aoi_footprint(app_config, project_root_path):
    """Determines the AOI footprint from config (GeoJSON or BBOX)."""
    default_config = app_config['DEFAULT']
    aoi_geojson_path_str = default_config.get('aoi_geojson_path', None)
    aoi_bbox_str = default_config.get('aoi_bbox', None)

    if aoi_geojson_path_str:
        # Paths in config are relative to project root or absolute
        aoi_path = Path(aoi_geojson_path_str)
        if not aoi_path.is_absolute():
            aoi_path = project_root_path / aoi_path
        
        if aoi_path.exists():
            try:
                logger.info(f"Using AOI from GeoJSON: {aoi_path}")
                return geojson_to_wkt(read_geojson(str(aoi_path)))
            except Exception as e:
                logger.error(f"Could not read or parse GeoJSON file '{aoi_path}': {e}")
                raise
        else:
            logger.warning(f"AOI GeoJSON file specified but not found: {aoi_path}. Checking BBOX.")
            # Fall through to BBOX if GeoJSON path is given but file not found
    
    if aoi_bbox_str: # Changed to 'if' instead of 'elif' to allow fallback
        try:
            coords = [float(c.strip()) for c in aoi_bbox_str.split(',')]
            if len(coords) != 4:
                raise ValueError("AOI BBOX must have 4 coordinates (lon_min, lat_min, lon_max, lat_max).")
            lon_min, lat_min, lon_max, lat_max = coords
            logger.info(f"Using AOI from BBOX: {lon_min}, {lat_min}, {lon_max}, {lat_max}")
            # Format for WKT POLYGON: "POLYGON((lon_min lat_min, lon_min lat_max, lon_max lat_max, lon_max lat_min, lon_min lat_min))"
            return f"POLYGON(({lon_min} {lat_min}, {lon_min} {lat_max}, {lon_max} {lat_max}, {lon_max} {lat_min}, {lon_min} {lat_min}))"
        except ValueError as e:
            logger.error(f"Invalid AOI BBOX format in config: {e}")
            raise
    elif aoi_bbox_str:
        try:
            coords = [float(c.strip()) for c in aoi_bbox_str.split(',')]
            if len(coords) != 4:
                raise ValueError("AOI BBOX must have 4 coordinates (lon_min, lat_min, lon_max, lat_max).")
            lon_min, lat_min, lon_max, lat_max = coords
            logging.info(f"Using AOI from BBOX: {lon_min}, {lat_min}, {lon_max}, {lat_max}")
            # Format for WKT POLYGON: "POLYGON((lon_min lat_min, lon_min lat_max, lon_max lat_max, lon_max lat_min, lon_min lat_min))"
            return f"POLYGON(({lon_min} {lat_min}, {lon_min} {lat_max}, {lon_max} {lat_max}, {lon_max} {lat_min}, {lon_min} {lat_min}))"
        except ValueError as e:
            logging.error(f"Invalid AOI BBOX format in config: {e}")
            raise
    else:
        raise ValueError("AOI not defined. Provide 'aoi_geojson_path' or 'aoi_bbox' in config.")

def download_sentinel2_data(api, footprint, start_date_str, end_date_str, product_type, cloud_cover, download_dir):
    """
    Queries and downloads Sentinel-2 products.
    """
    Path(download_dir).mkdir(parents=True, exist_ok=True)
    logging.info(f"Searching for {product_type} products...")
    logging.info(f"AOI WKT: {footprint[:100]}...") # Log a snippet of WKT
    logging.info(f"Date Range: {start_date_str} to {end_date_str}")
    logging.info(f"Max Cloud Cover: {cloud_cover}%")

    try:
        products = api.query(
            footprint,
            date=(start_date_str, end_date_str),
            platformname='Sentinel-2',
            producttype=product_type, # e.g., S2MSI2A (Level-2A) or S2MSI1C (Level-1C)
            cloudcoverpercentage=(0, cloud_cover)
        )
    except SentinelsatAPIError as e:
        logging.error(f"API Error during product query: {e}")
        if "Too Many Requests" in str(e) or "429" in str(e):
            logging.error("Consider adding a delay or checking API limits if this persists.")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred during product query: {e}")
        return

    if not products:
        logging.warning("No products found matching your criteria.")
        return

    products_gdf = api.to_geodataframe(products)
    logging.info(f"Found {len(products_gdf)} products.")
    
    # Sort products by ingestion date or cloud cover to prioritize downloads if needed
    products_gdf = products_gdf.sort_values(['ingestiondate'], ascending=[False]) # Download newest first

    for product_id, product_info in products_gdf.iterrows():
        title = product_info['title']
        logging.info(f"Attempting to download product: {title} (ID: {product_id})")
        logging.info(f"  Cloud Cover: {product_info.get('cloudcoverpercentage', 'N/A')}%")
        logging.info(f"  Ingestion Date: {product_info.get('ingestiondate', 'N/A')}")
        
        # Check if already downloaded (simple check by directory name)
        product_path = Path(download_dir) / title
        if product_path.exists() and product_path.with_suffix(".SAFE").exists(): # Sentinel products are .SAFE folders
             # A more robust check would be to verify integrity, e.g. using `api.is_online(product_id)`
             # and then checking if a specific file (like manifest.safe) exists and is not corrupt.
             # Sentinelsat also has a `check_files` option in `api.download` but it requires more setup.
            logging.info(f"Product {title} already exists in {download_dir}. Skipping download.")
            continue

        try:
            api.download(product_id, directory_path=download_dir)
            logging.info(f"Successfully downloaded: {title}")
        except SentinelsatAPIError as e:
            logging.error(f"API Error downloading {title} (ID: {product_id}): {e}")
            if "Product_is_not_online" in str(e) or "offline" in str(e).lower():
                logging.warning(f"Product {title} is offline. It might become available later. Skipping.")
            elif "MD5 checksum" in str(e):
                logging.error(f"MD5 checksum mismatch for {title}. Download may be corrupt. Consider retrying.")
                # Optionally, delete the corrupted download here
                # if product_path.with_suffix(".zip").exists(): # Downloads are often .zip
                #    product_path.with_suffix(".zip").unlink()
            else:
                logging.error(f"An unexpected SentinelsatAPIError occurred: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred downloading {title} (ID: {product_id}): {e}")

    logging.info("Download process finished.")

# --- Main Execution ---
if __name__ == "__main__":
    # Determine project root assuming script is in OpenAI_LostCityZ_AmazonArchaeology/scripts/pipeline_type/
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    try:
        # Pass the script's directory to load_config so it can resolve CONFIG_FILE_PATH correctly
        app_config = load_config(SCRIPT_DIR, CONFIG_FILE_PATH) 
    except FileNotFoundError as e:
        # This path is relative to where the script is executed from, not necessarily script location
        # If run from project root: python scripts/satellite_pipeline/acquire_sentinel2.py
        # then CONFIG_FILE_PATH should be "config/config.ini"
        # Let's adjust load_config to be more robust or assume script is run from project root.
        # For now, the updated load_config tries to resolve from script dir.
        # The logger might not be set up yet if config loading fails this early.
        print(f"FATAL: Configuration file not found. Error: {e}")
        exit(1)

    default_config = app_config['DEFAULT']
    
    # Setup logging (paths from config are relative to project root as per config comments)
    log_dir_config = default_config.get('log_dir', 'logs') # Default to 'logs' in project root
    log_file_name_config = default_config.get('satellite_log_file_name', 'satellite_pipeline.log')
    
    log_dir_abs = PROJECT_ROOT / log_dir_config
    setup_logging(log_dir_abs, log_file_name_config)

    logger.info("--- Starting Sentinel-2 Data Acquisition ---")

    api_user = default_config.get('api_user')
    api_password = default_config.get('api_password')
    api_url = default_config.get('api_url')

    if not api_user or not api_password or not api_url or \
       api_user == 'YOUR_USERNAME_HERE' or api_password == 'YOUR_PASSWORD_HERE':
        logger.error("API credentials (api_user, api_password) or api_url are not set or are default values in config.ini. Please update them.")
        exit(1)

    try:
        api = SentinelAPI(api_user, api_password, api_url)
        logger.info(f"Successfully connected to API: {api_url}")
    except SentinelsatAPIError as e:
        logger.error(f"Failed to connect to Sentinel API at {api_url}: {e}")
        logger.error("Please check your API credentials, the API URL, and your internet connection.")
        exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred during API connection: {e}")
        exit(1)

    try:
        footprint_wkt = get_aoi_footprint(app_config, PROJECT_ROOT)
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"AOI configuration error: {e}")
        exit(1)

    start_date = default_config.get('start_date')
    end_date = default_config.get('end_date')
    cloud_cover = default_config.getint('cloud_cover_percentage', 10)
    
    base_raw_dir_config = default_config.get('base_raw_data_dir', 'data')
    s2_raw_suffix_config = default_config.get('s2_raw_suffix', 'sentinel2/raw')
    raw_data_dir_abs = PROJECT_ROOT / base_raw_dir_config / s2_raw_suffix_config
    
    product_type = default_config.get('product_type', 'S2MSI2A')

    # Validate date formats
    try:
        datetime.strptime(start_date, '%Y%m%d')
        datetime.strptime(end_date, '%Y%m%d')
    except ValueError:
        logger.error("Invalid date format in config.ini. Please use YYYYMMDD (e.g., 20230101).")
        exit(1)

    download_sentinel2_data(api, footprint_wkt, start_date, end_date, product_type, cloud_cover, raw_data_dir)

    logger.info("--- Sentinel-2 Data Acquisition Finished ---")
