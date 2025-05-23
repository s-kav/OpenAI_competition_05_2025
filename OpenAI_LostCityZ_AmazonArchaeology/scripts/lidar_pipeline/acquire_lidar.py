import configparser
import logging
import os
import requests
from pathlib import Path
from urllib.parse import urlparse

# --- Configuration and Logging Setup ---
CONFIG_FILE_PATH = "../config/config.ini" # Adjusted path
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__) # Define logger at module level

def setup_logging(log_dir_path, log_file_name):
    """Sets up logging configuration."""
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

# --- Main Acquisition Logic ---
def download_file(url, target_dir):
    """Downloads a file from a URL to a target directory."""
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    filename = Path(urlparse(url).path).name
    target_filepath = Path(target_dir) / filename

    if target_filepath.exists():
        logging.info(f"File {filename} already exists in {target_dir}. Skipping download.")
        return True

    try:
        logging.info(f"Downloading {url} to {target_filepath}...")
        response = requests.get(url, stream=True, timeout=300) # 5 min timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        
        with open(target_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Successfully downloaded {filename}.")
        return True
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error downloading {url}: {e}")
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection error downloading {url}: {e}")
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout downloading {url}: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")
    except IOError as e:
        logging.error(f"File system error writing {target_filepath}: {e}")
    return False

# --- Main Execution ---
if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent.parent

    try:
        app_config = load_config(SCRIPT_DIR, CONFIG_FILE_PATH)
    except FileNotFoundError as e:
        print(f"FATAL: Configuration file not found. Error: {e}")
        exit(1)

    default_config = app_config['DEFAULT']
    lidar_config = app_config.get('LIDAR') # Use .get to avoid error if section missing

    if not lidar_config:
        print("FATAL: [LIDAR] section not found in configuration file.") # Logger not set yet
        exit(1)

    log_dir_config = default_config.get('log_dir', 'logs') 
    log_file_name_config = lidar_config.get('lidar_log_file_name', default_config.get('lidar_log_file_name', 'lidar_pipeline.log'))
    log_dir_abs = PROJECT_ROOT / log_dir_config
    setup_logging(log_dir_abs, log_file_name_config) # logger is globally available

    logger.info("--- Starting LiDAR Data Acquisition ---")

    lidar_data_urls_str = lidar_config.get('lidar_data_urls', '')
    if not lidar_data_urls_str.strip(): # Check if string is empty or only whitespace
        logger.warning("No LiDAR data URLs found in 'lidar_data_urls' in config.ini. Nothing to download.")
        logger.info("--- LiDAR Data Acquisition Finished (No URLs) ---")
        exit(0)
    
    lidar_urls = [url.strip() for url in lidar_data_urls_str.splitlines() if url.strip()]
    if not lidar_urls: # After stripping, list might be empty
        logger.warning("LiDAR data URLs list is empty after parsing. Nothing to download.")
        logger.info("--- LiDAR Data Acquisition Finished (No URLs) ---")
        exit(0)

    base_raw_dir_config = default_config.get('base_raw_data_dir', 'data')
    lidar_raw_suffix_config = lidar_config.get('lidar_raw_suffix', 'lidar/raw')
    raw_lidar_dir_abs = PROJECT_ROOT / base_raw_dir_config / lidar_raw_suffix_config
    
    logger.info(f"Raw LiDAR data will be downloaded to: {raw_lidar_dir_abs}")
    Path(raw_lidar_dir_abs).mkdir(parents=True, exist_ok=True)

    download_count = 0
    error_count = 0
    for url in lidar_urls:
        if download_file(url, raw_lidar_dir_abs): # Use absolute path
            download_count += 1
        else:
            error_count += 1
            # download_file function already logs errors for the specific URL
            # logger.warning(f"Failed to download from URL: {url}") # Redundant

    if error_count > 0:
        logger.warning(f"Finished LiDAR acquisition with {error_count} download errors.")
    if download_count == 0 and error_count == 0 and lidar_urls: # Check if lidar_urls was not empty to begin with
        logger.info("All specified LiDAR files were already present or no new valid URLs provided. No new downloads.")
    elif download_count > 0 :
         logger.info(f"Successfully downloaded/verified {download_count} LiDAR files.")


    logger.info("--- LiDAR Data Acquisition Finished ---")
