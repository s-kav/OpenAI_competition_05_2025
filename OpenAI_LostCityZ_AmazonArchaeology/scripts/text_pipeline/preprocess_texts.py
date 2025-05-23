import configparser
import logging
import os
import re
import json
from pathlib import Path
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdfminer.layout import LAParams
import ftfy
from langdetect import detect as langdetect_detect, LangDetectException
import shutil # For checking tesseract path

# Attempt to import OCR related libraries, but don't make them hard dependencies
try:
    import pytesseract
    from PIL import Image
    # pdf2image is often used to convert PDF pages to images for OCR
    # It requires poppler installed on the system
    from pdf2image import convert_from_path as pdf2image_convert
    OCR_CAPABLE = True
except ImportError:
    OCR_CAPABLE = False
    # logging.warning("pytesseract, Pillow, or pdf2image not installed. OCR capabilities will be disabled.")


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

# --- Text Processing Functions ---

def extract_text_from_pdf_native(pdf_path, output_txt_path):
    """Extracts text from a PDF using pdfminer.six."""
    try:
        logger.info(f"Extracting text natively from PDF: {pdf_path.name}")
        # LAParams can be tuned for better layout analysis if needed
        # laparams = LAParams(line_margin=0.5, word_margin=0.1, char_margin=2.0, boxes_flow=0.5)
        text_content = pdfminer_extract_text(str(pdf_path)) #, laparams=laparams)
        
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        logger.info(f"Successfully extracted text natively to: {output_txt_path.name}")
        return True
    except Exception as e:
        logger.error(f"pdfminer.six failed to extract text from {pdf_path.name}: {e}", exc_info=True)
        return False

def extract_text_from_pdf_ocr(pdf_path, output_txt_path, tesseract_cmd, ocr_langs, dpi, ocr_intermediate_dir):
    """Extracts text from a PDF using OCR (Tesseract)."""
    if not OCR_CAPABLE:
        logger.error(f"OCR libraries (pytesseract, Pillow, pdf2image) not available. Cannot OCR {pdf_path.name}.")
        return False
    if tesseract_cmd and Path(tesseract_cmd).is_file():
        pytesseract.tesseract_cmd = tesseract_cmd
    elif shutil.which("tesseract"): # Check if tesseract is in PATH
         pytesseract.tesseract_cmd = "tesseract"
    else:
        logger.error("Tesseract OCR command not found or configured. Please set 'tesseract_cmd_path' in config or ensure Tesseract is in system PATH.")
        return False

    try:
        logger.info(f"Attempting OCR for PDF: {pdf_path.name} using languages: {ocr_langs}, DPI: {dpi}")
        Path(ocr_intermediate_dir).mkdir(parents=True, exist_ok=True)
        
        # Convert PDF to list of images
        images = pdf2image_convert(pdf_path, dpi=dpi, output_folder=ocr_intermediate_dir, fmt='png', thread_count=2) # thread_count can be tuned
        
        full_text_content = []
        for i, image_path in enumerate(images): # images is a list of Path objects to the temp image files
            logger.info(f"OCR processing page {i+1} of {len(images)} for {pdf_path.name} (image: {Path(image_path).name})")
            try:
                page_text = pytesseract.image_to_string(Image.open(image_path), lang=ocr_langs)
                full_text_content.append(page_text)
            except pytesseract.TesseractError as te:
                logger.error(f"Tesseract error on page {i+1} of {pdf_path.name}: {te}")
            except Exception as e_img:
                logger.error(f"Error processing image {Path(image_path).name} for OCR: {e_img}")
            finally:
                if Path(image_path).exists(): # Clean up intermediate image file
                    Path(image_path).unlink()
        
        if not full_text_content:
            logger.warning(f"OCR processing yielded no text for {pdf_path.name}.")
            # Create an empty .txt file to mark as processed
            output_txt_path.touch()
            return False # Or True if empty file is acceptable result of OCR

        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(full_text_content)) # Add double newline as page separator
        logger.info(f"Successfully extracted text via OCR to: {output_txt_path.name}")
        return True

    except Exception as e:
        logger.error(f"OCR process failed for {pdf_path.name}: {e}", exc_info=True)
        if "Unable to get page count" in str(e) or "PDFInfoNotInstalledError" in str(e):
             logger.error("This OCR error might be due to Poppler utilities not being installed or not found in PATH.")
             logger.error("Please install Poppler (e.g., 'conda install -c conda-forge poppler' or 'sudo apt-get install poppler-utils')")
        return False


def clean_text_content(text, to_lowercase=True, custom_patterns_json="[]"):
    """Cleans text content: ftfy, whitespace, optional lowercase, custom regex."""
    if not text:
        return ""
    
    # Fix unicode issues like mojibake
    text = ftfy.fix_text(text)
    
    # Normalize whitespace: replace multiple spaces/tabs/newlines with a single space,
    # but try to preserve paragraph breaks (double newlines become single newlines here for now).
    # More sophisticated paragraph segmentation could be done later.
    text = re.sub(r'[ \t\r\f\v]+', ' ', text) # Replace various space chars with single space
    text = re.sub(r'\n[ \t]*\n', '\n', text) # Reduce multiple newlines with spaces in between to single newline
    text = re.sub(r'\n+', '\n', text) # Reduce multiple newlines to single newline
    text = text.strip()

    if to_lowercase:
        text = text.lower()

    try:
        custom_patterns = json.loads(custom_patterns_json)
        for pattern in custom_patterns:
            try:
                text = re.sub(pattern, '', text)
            except re.error as e:
                logger.warning(f"Invalid regex pattern in custom_remove_patterns_json: '{pattern}'. Error: {e}")
    except json.JSONDecodeError:
        logger.warning("Could not parse 'custom_remove_patterns_json'. Ensure it's a valid JSON list of strings.")
        
    return text

def identify_language(text_content):
    """Identifies language of the text. Returns lang code (e.g., 'en') or None."""
    if not text_content or len(text_content.strip()) < 20: # Too short to reliably detect
        logger.debug("Text too short for language detection or empty.")
        return None
    try:
        lang = langdetect_detect(text_content)
        return lang
    except LangDetectException as e: # Can occur if text is too short or ambiguous
        logger.warning(f"Language detection failed: {e}. Content snippet: '{text_content[:100]}...'")
        return None


# --- Main Execution ---
if __name__ == "__main__":
    try:
        config = load_config()
    except FileNotFoundError as e:
        try:
            config = load_config("config.ini") # Fallback
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

    logger.info("--- Starting Textual Data Preprocessing ---")

    base_raw_dir_raw = default_config.get('base_raw_data_dir', '../../data')
    text_raw_suffix = text_config.get('text_raw_suffix', 'textual/raw')
    raw_texts_dir = (script_dir / base_raw_dir_raw / text_raw_suffix).resolve()

    base_processed_dir_raw = default_config.get('base_processed_data_dir', '../../data')
    text_processed_suffix = text_config.get('text_processed_suffix', 'textual/processed')
    processed_texts_dir = (script_dir / base_processed_dir_raw / text_processed_suffix).resolve()
    
    ocr_intermediate_suffix = text_config.get('ocr_intermediate_suffix', 'textual/ocr_intermediate')
    ocr_intermediate_dir_path = (script_dir / base_raw_dir_raw / ocr_intermediate_suffix).resolve()


    Path(processed_texts_dir).mkdir(parents=True, exist_ok=True)
    logger.info(f"Raw textual data source: {raw_texts_dir}")
    logger.info(f"Processed textual data will be saved to: {processed_texts_dir}")
    if OCR_CAPABLE:
        logger.info(f"OCR intermediate files (if any) will be in: {ocr_intermediate_dir_path}")


    force_reprocess_raw = text_config.getboolean('force_reprocess_raw', False) # From acquire_texts, applies to HTML->TXT here
    force_reprocess_processed = text_config.getboolean('force_reprocess_processed', False)

    # Config for text cleaning and PDF processing
    clean_lowercase = text_config.getboolean('clean_text_to_lowercase', True)
    custom_patterns = text_config.get('custom_remove_patterns_json', "[]")
    pdf_extract_method = text_config.get('pdf_extraction_method', 'native').lower()
    tesseract_cmd = text_config.get('tesseract_cmd_path', None)
    ocr_langs_conf = text_config.get('ocr_languages', 'eng')
    pdf_ocr_render_dpi = text_config.getint('pdf_ocr_dpi', 300)


    # Determine which source files were marked as PDF_OCR during acquisition
    # This information isn't directly passed, so we rely on pdf_extraction_method or user knowledge
    # We iterate through raw_texts_dir content.

    processed_count = 0
    for raw_file_path in raw_texts_dir.iterdir():
        if raw_file_path.is_dir() or raw_file_path.name.startswith('.'): # Skip directories and hidden files
            continue

        logger.info(f"Found raw file: {raw_file_path.name}")
        output_base_name = raw_file_path.stem.replace("_raw", "") # If it was _raw.html
        
        # Path for the text file that will be cleaned (either from PDF or already .txt)
        text_to_clean_path = None
        # Path for the final processed (cleaned) text file
        processed_txt_final_path = processed_texts_dir / f"{output_base_name}_processed.txt"
        lang_file_path = processed_texts_dir / f"{output_base_name}_processed.lang"

        if not force_reprocess_processed and processed_txt_final_path.exists() and lang_file_path.exists():
            logger.info(f"Processed file {processed_txt_final_path.name} and lang file already exist. Skipping.")
            processed_count +=1
            continue

        # PDF Processing
        if raw_file_path.suffix.lower() == '.pdf':
            # This is the .txt file derived from PDF, placed in processed_dir before cleaning
            intermediate_pdf_extracted_txt_path = processed_texts_dir / f"{output_base_name}_pdfextract.txt"
            
            extraction_done = False
            if pdf_extract_method == 'native':
                extraction_done = extract_text_from_pdf_native(raw_file_path, intermediate_pdf_extracted_txt_path)
            elif pdf_extract_method == 'ocr_only':
                if not OCR_CAPABLE: logger.error("OCR method selected but OCR libraries are not available."); continue
                extraction_done = extract_text_from_pdf_ocr(raw_file_path, intermediate_pdf_extracted_txt_path, 
                                                            tesseract_cmd, ocr_langs_conf, pdf_ocr_render_dpi, 
                                                            ocr_intermediate_dir_path)
            else: # Default to native if method unknown
                logger.warning(f"Unknown pdf_extraction_method '{pdf_extract_method}'. Defaulting to 'native'.")
                extraction_done = extract_text_from_pdf_native(raw_file_path, intermediate_pdf_extracted_txt_path)

            if extraction_done and intermediate_pdf_extracted_txt_path.exists():
                text_to_clean_path = intermediate_pdf_extracted_txt_path
            else:
                logger.error(f"Failed to extract text from PDF {raw_file_path.name}. Skipping further processing for this file.")
                # Create empty files to mark as "processed" with error
                processed_txt_final_path.touch()
                lang_file_path.touch()
                continue
        
        # TXT file (either original .txt or .txt extracted from HTML by acquire_texts.py)
        elif raw_file_path.suffix.lower() == '.txt':
            text_to_clean_path = raw_file_path
        
        else: # Other raw file types not directly processed (e.g. _raw.html)
            logger.info(f"Skipping non-PDF/non-TXT file in raw directory: {raw_file_path.name}")
            continue

        # --- Cleaning and Language ID for the text_to_clean_path ---
        if text_to_clean_path and text_to_clean_path.exists():
            logger.info(f"Processing text file for cleaning: {text_to_clean_path.name}")
            try:
                with open(text_to_clean_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                logger.error(f"Could not read text file {text_to_clean_path.name}: {e}. Skipping.")
                # Create empty files to mark as "processed" with error
                processed_txt_final_path.touch()
                lang_file_path.touch()
                continue

            cleaned_content = clean_text_content(content, clean_lowercase, custom_patterns)
            
            with open(processed_txt_final_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            logger.info(f"Saved cleaned text to: {processed_txt_final_path.name}")

            language = identify_language(cleaned_content[:5000]) # Detect on first 5k chars
            if language:
                with open(lang_file_path, 'w', encoding='utf-8') as f:
                    f.write(language)
                logger.info(f"Identified language '{language}' for {processed_txt_final_path.name} and saved to {lang_file_path.name}")
            else:
                logger.warning(f"Could not identify language for {processed_txt_final_path.name}. Lang file not created.")
                if lang_file_path.exists(): lang_file_path.unlink() # Remove if exists from previous failed run

            # Clean up intermediate PDF extracted text file if it's different from raw .txt file
            if text_to_clean_path != raw_file_path and text_to_clean_path.exists() and text_to_clean_path.name.endswith("_pdfextract.txt"):
                logger.info(f"Removing intermediate PDF extracted text: {text_to_clean_path.name}")
                text_to_clean_path.unlink()
            
            processed_count +=1
        else:
            logger.warning(f"No text content found to process for base name: {output_base_name} (derived from {raw_file_path.name})")
            # Create empty files to mark as "processed" with error
            processed_txt_final_path.touch()
            lang_file_path.touch()


    if processed_count == 0:
        logger.info("No new text files were processed in this run.")
    else:
        logger.info(f"Successfully processed or verified {processed_count} text sources.")
    logger.info("--- Textual Data Preprocessing Finished ---")
