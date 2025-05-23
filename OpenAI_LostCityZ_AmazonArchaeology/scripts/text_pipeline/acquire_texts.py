import configparser
import logging
import os
import requests
import trafilatura
from pathlib import Path
from urllib.parse import urlparse, unquote
import re

# --- Configuration and Logging Setup ---
CONFIG_FILE_PATH = "../satellite_pipeline/config.ini" # Assuming shared config
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

def setup_logging(log_dir_path, log_file_name):
    Path(log_dir_path).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir_path) / log_file_name
    logger_root = logging.getLogger()
    for handler in logger_root.handlers[:]:
        logger_root.removeHandler(handler)
    logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT, filemode='a')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(console_handler)
    return logging.getLogger(__name__)

def load_config(config_path=CONFIG_FILE_PATH):
    config = configparser.ConfigParser(interpolation=None, allow_no_value=True)
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    config.read(config_path)
    return config

def sanitize_filename(filename):
    """Sanitizes a filename by removing or replacing invalid characters."""
    # Decode URL encoding
    filename = unquote(filename)
    # Remove or replace invalid chars
    filename = re.sub(r'[<>:"/\\|?*\s+,;=]', '_', filename)
    # Reduce multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Limit length
    filename = filename[:100]
    return filename

def download_and_extract(url, source_type, output_filename_base, raw_dir_path):
    """Downloads content from URL, extracts text if HTML, and saves."""
    Path(raw_dir_path).mkdir(parents=True, exist_ok=True)

    try:
        headers = { # Be a good internet citizen
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=60) # 60s timeout
        response.raise_for_status()
        logger.info(f"Successfully fetched URL: {url} (status: {response.status_code})")

        content_type_header = response.headers.get('Content-Type', '').lower()
        
        # Infer type if not explicitly given
        if not source_type:
            if '.pdf' in url.lower() or 'application/pdf' in content_type_header:
                source_type = 'PDF'
            elif '.txt' in url.lower() or 'text/plain' in content_type_header:
                source_type = 'TXT'
            elif 'text/html' in content_type_header or url.lower().endswith(('.html', '.htm')):
                source_type = 'HTML'
            else: # Default to HTML if unsure, trafilatura might handle it or fail gracefully
                logger.warning(f"Could not infer type for {url}, attempting as HTML.")
                source_type = 'HTML'
        
        source_type = source_type.upper()

        # Determine filenames
        if not output_filename_base: # If no custom name, derive from URL
            parsed_url_path = Path(urlparse(url).path)
            # Use the last part of the path, or if that's empty (e.g. domain only), use domain
            filename_stem = parsed_url_path.stem if parsed_url_path.stem else Path(urlparse(url).netloc).stem
            output_filename_base = sanitize_filename(filename_stem)
            if not output_filename_base: # Still empty e.g. if domain was just 'com'
                output_filename_base = "unknown_source"


        raw_filepath = None
        extracted_txt_filepath = raw_dir_path / f"{output_filename_base}.txt" # Default for extracted

        if source_type == 'HTML':
            raw_filepath = raw_dir_path / f"{output_filename_base}_raw.html"
            with open(raw_filepath, 'wb') as f:
                f.write(response.content)
            logger.info(f"Saved raw HTML: {raw_filepath.name}")
            
            # Extract text using Trafilatura
            # include_comments=False, include_tables=False are defaults
            # favor_recall=True can sometimes get more text but might be noisier
            extracted_text = trafilatura.extract(response.content, url=url,
                                                 include_formatting=False, # Keep paragraph structure
                                                 include_links=False, # Remove hyperlinks text
                                                 deduplicate=True) 
            if extracted_text:
                with open(extracted_txt_filepath, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                logger.info(f"Extracted text from HTML and saved to: {extracted_txt_filepath.name}")
            else:
                logger.warning(f"Trafilatura extracted no main text from HTML: {url}. Raw HTML is saved.")
                # Create an empty .txt file to signal attempt
                extracted_txt_filepath.touch()


        elif source_type == 'PDF' or source_type == 'PDF_OCR': # PDF_OCR handled in preprocessing
            raw_filepath = raw_dir_path / f"{output_filename_base}.pdf"
            with open(raw_filepath, 'wb') as f:
                f.write(response.content)
            logger.info(f"Saved PDF: {raw_filepath.name}")
            # We don't create a .txt file here for PDFs; that's preprocessing's job.

        elif source_type == 'TXT':
            # For TXT, the raw file is the text file itself.
            raw_filepath = extracted_txt_filepath # Save directly as .txt
            with open(raw_filepath, 'wb') as f: # Write as binary first to handle encoding issues later if any
                f.write(response.content)
            logger.info(f"Saved TXT: {raw_filepath.name}")
        
        else:
            logger.error(f"Unsupported source type '{source_type}' for URL: {url}")
            return False
        
        return True

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error for {url}: {e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error for {url}: {e}")
    except requests.exceptions.Timeout:
        logger.error(f"Timeout for {url}.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for {url}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred for {url}: {e}", exc_info=True)
    return False

# --- Main Execution ---
if __name__ == "__main__":
    try:
        config = load_config()
    except FileNotFoundError as e:
        try:
            config = load_config("config.ini") # Fallback for running from script dir
        except FileNotFoundError:
            print(f"FATAL: Configuration file not found. Error: {e}")
            exit(1)

    default_config = config['DEFAULT']
    text_config = config.get('TextualData')

    if not text_config:
        print("FATAL: [TextualData] section not found in configuration file.")
        exit(1)

    script_dir = Path(__file__).resolve().parent
    log_dir_raw = default_config.get('log_dir', '../../logs')
    log_dir = (script_dir / log_dir_raw).resolve()
    log_file_name = text_config.get('text_pipeline_log_file_name', 
                                   default_config.get('text_pipeline_log_file_name', 'text_pipeline.log'))
    logger = setup_logging(log_dir, log_file_name)

    logger.info("--- Starting Textual Data Acquisition ---")

    text_sources_str = text_config.get('text_data_sources', '')
    if not text_sources_str.strip():
        logger.warning("No text data sources found in 'text_data_sources' in config.ini. Nothing to download.")
        logger.info("--- Textual Data Acquisition Finished (No URLs) ---")
        exit(0)

    # Parse sources: URL | TYPE (Optional) | Custom_Filename (Optional)
    sources = []
    for line in text_sources_str.splitlines():
        line = line.strip()
        if not line or line.startswith('#'): # Skip empty lines and comments
            continue
        parts = [p.strip() for p in line.split('|')]
        url = parts[0]
        src_type = parts[1] if len(parts) > 1 and parts[1] else None
        custom_filename = parts[2] if len(parts) > 2 and parts[2] else None
        if url:
            sources.append({'url': url, 'type': src_type, 'custom_fn': custom_filename})
        else:
            logger.warning(f"Skipping invalid source line (no URL): {line}")


    base_raw_dir_raw = default_config.get('base_raw_data_dir', '../../data')
    text_raw_suffix = text_config.get('text_raw_suffix', 'textual/raw')
    raw_texts_dir = (script_dir / base_raw_dir_raw / text_raw_suffix).resolve()
    
    logger.info(f"Raw textual data will be downloaded/saved to: {raw_texts_dir}")
    Path(raw_texts_dir).mkdir(parents=True, exist_ok=True)

    download_count = 0
    error_count = 0
    force_reprocess_raw = text_config.getboolean('force_reprocess_raw', False)

    for source_entry in sources:
        url = source_entry['url']
        source_type = source_entry['type']
        custom_fn_base = source_entry['custom_fn']

        # Construct expected output path to check if it needs reprocessing
        # For HTML, the primary output of this script is the extracted .txt
        # For PDF/TXT, it's the raw .pdf/.txt itself.
        # This check needs to be more nuanced or handled primarily by preprocess_texts.py
        # For now, `force_reprocess_raw` will re-download and re-extract HTML.
        # It won't re-download PDF/TXT if the raw file exists, unless force_reprocess_raw is true.

        # Simplified check: if the main expected output (e.g. .txt from HTML, or .pdf) exists, skip
        # A more robust check would be in preprocess_texts.py
        
        # Determine a base filename for checking existence, even before full sanitization
        temp_output_filename_base = custom_fn_base if custom_fn_base else Path(urlparse(url).path).stem
        temp_output_filename_base = sanitize_filename(temp_output_filename_base if temp_output_filename_base else "unknown_source")

        # Check if primary output already exists and if we should skip
        # For HTML, the extracted .txt is the key output of this script.
        # For PDF, the .pdf is the key output. For TXT, the .txt is the key output.
        expected_output_path_check = None
        stype_upper = source_type.upper() if source_type else ""
        
        if stype_upper == 'HTML':
            expected_output_path_check = raw_texts_dir / f"{temp_output_filename_base}.txt"
        elif stype_upper == 'PDF' or stype_upper == 'PDF_OCR':
            expected_output_path_check = raw_texts_dir / f"{temp_output_filename_base}.pdf"
        elif stype_upper == 'TXT':
             expected_output_path_check = raw_texts_dir / f"{temp_output_filename_base}.txt"
        # If type is unknown, it will be inferred, likely as HTML.

        if not force_reprocess_raw and expected_output_path_check and expected_output_path_check.exists():
            logger.info(f"Primary output for {url} (e.g., {expected_output_path_check.name}) already exists and force_reprocess_raw is false. Skipping acquisition.")
            download_count +=1 # Count as "processed" or "accounted for"
            continue
        
        if download_and_extract(url, source_type, custom_fn_base, raw_texts_dir):
            download_count += 1
        else:
            error_count += 1
            logger.warning(f"Failed to acquire or extract from URL: {url}")

    if error_count > 0:
        logger.warning(f"Finished text acquisition with {error_count} errors.")
    if download_count == 0 and error_count == 0 and sources:
        logger.info("All specified text sources were already processed or no new files acquired.")
    elif download_count > 0:
         logger.info(f"Successfully acquired/extracted or verified {download_count} text sources.")

    logger.info("--- Textual Data Acquisition Finished ---")
