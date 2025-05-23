# Textual Data Acquisition and Preprocessing Pipeline

This pipeline provides scripts to acquire textual data from various online sources (direct text, HTML, PDF) and preprocess it into a clean, plain text format suitable for Natural Language Processing (NLP) tasks.

## Features

*   **Data Acquisition (`acquire_texts.py`):**
    *   Fetches data from a list of URLs provided in the configuration file.
    *   Supports direct download for `.txt` files.
    *   Downloads HTML content and attempts to extract the main article/text using `trafilatura` to remove boilerplate (navigation, ads, sidebars, etc.). Saves both raw HTML and extracted TXT.
    *   Downloads PDF files directly.
    *   Saves downloaded content into a structured raw data directory, preserving original formats where possible and saving extracted text as `.txt`.
    *   Includes logging of activities and basic error handling (e.g., for broken URLs, network issues).
*   **Data Preprocessing (`preprocess_texts.py`):**
    *   **PDF to Text Conversion:** Converts downloaded PDF files to plain text using `pdfminer.six`.
    *   **OCR (Optical Character Recognition):** (Planned/Conceptual) For image-based PDFs or scanned documents, Tesseract OCR (via `pytesseract`) would be used. This feature requires Tesseract to be installed. The current implementation may include a placeholder or basic structure for this.
    *   **Text Cleaning:**
        *   Applies `ftfy` to fix Unicode inconsistencies (e.g., mojibake).
        *   Normalizes whitespace (multiple spaces, tabs, newlines).
        *   Optionally converts text to lowercase.
        *   Optionally removes custom-defined special characters or patterns (configurable).
    *   **Language Identification:** Identifies the language of each processed text document using `langdetect` and saves this as a `.lang` metadata file.
    *   **Basic Structuring (Paragraphs):** Retains paragraph breaks from extracted/converted text.
    *   Saves processed plain text files and associated metadata.
    *   Logs all processing steps.

## Setup

### 1. Dependencies

Install the required Python libraries:

```bash
pip install requests trafilatura pdfminer.six ftfy langdetect Pillow # Pillow is a Tesseract dependency
# For OCR (optional, if fully implemented and used):
# pip install pytesseract
```

**Additionally, for OCR functionality (if used):**

*   **Tesseract OCR Engine:** You must install Tesseract OCR on your system.
    *   **Windows:** Download the installer from the official Tesseract at UB Mannheim page ([https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)). Ensure to add Tesseract to your system PATH during installation or note the installation path for the config file.
    *   **Linux (Ubuntu/Debian):** `sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-por tesseract-ocr-spa` (install language packs as needed, e.g., `eng` for English, `por` for Portuguese, `spa` for Spanish).
    *   **macOS:** `brew install tesseract tesseract-lang`
    *   Verify installation by running `tesseract --version` in your terminal.

### 2. Configuration File

Update your main `config.ini` file (e.g., the one in `scripts/satellite_pipeline/` or a central `scripts/config.ini`) with a `[TextualData]` section.

Example `config.ini` additions:

```ini
[DEFAULT]
# ... (existing DEFAULT settings like log_dir)
# Ensure log_dir is defined. text_pipeline_log_file_name can be specific.
text_pipeline_log_file_name = text_pipeline.log

[TextualData]
# List of URLs to fetch. Specify type if known, otherwise script will try to infer.
# Supported types for explicit definition: TXT, HTML, PDF, PDF_OCR (for PDFs that need OCR)
# If type is not given, it's inferred from URL extension or by attempting HTML/PDF parsing.
text_data_sources =
    # URL | TYPE (Optional) | Custom_Output_Filename (Optional, without extension)
    https://www.gutenberg.org/files/1342/1342-0.txt | TXT | pride_and_prejudice
    https://example-news-site.com/article-on-amazon-discovery | HTML | example_amazon_article
    https://arxiv.org/pdf/2301.00001.pdf | PDF | arxiv_paper_2301_00001
    # https://example.com/scanned_report.pdf | PDF_OCR | scanned_report_to_ocr

# Output Directories (relative to script location, e.g. scripts/text_pipeline/)
# These will be appended to base_raw_data_dir and base_processed_data_dir from [DEFAULT] if those exist
# Otherwise, they are relative to the script's current working directory.
text_raw_suffix = textual/raw
text_processed_suffix = textual/processed
ocr_output_suffix = textual/ocr # For text extracted via OCR

# Preprocessing Settings
force_reprocess_raw = false # If true, will re-extract text from raw HTML/PDF even if .txt exists in raw
force_reprocess_processed = false # If true, will re-clean text even if processed .txt exists

clean_text_to_lowercase = true
# Custom characters/patterns to remove (JSON list of regex patterns). Applied after basic cleaning.
# Example: ["\\b[A-Z]\\.\\s?", "[\\\"\\']"] # Removes single capital letters followed by dot; removes quotes
custom_remove_patterns_json = [] 
# Specific languages for Tesseract OCR, comma-separated (e.g., eng, por, spa)
# Only used if PDF_OCR type is specified and tesseract_path is set.
ocr_languages = eng

# Tesseract OCR Path (if not in system PATH or to specify a version)
# Example Windows: C:/Program Files/Tesseract-OCR/tesseract.exe
# Example Linux: /usr/bin/tesseract
tesseract_cmd_path = 
```

Ensure the output directories (e.g., `data/textual/raw`, `data/textual/processed`) exist or the scripts have permission to create them. You might need to create them relative to your `base_raw_data_dir` / `base_processed_data_dir` if using those from `[DEFAULT]`.

### 3. Logging

Logs will be written to the directory specified by `log_dir` in `[DEFAULT]` config, with the filename `text_pipeline_log_file_name`.

## Usage

1.  **Configure `config.ini`:**
    *   Add/update the `[TextualData]` section.
    *   Provide URLs for the texts you want to acquire, optionally with their types and custom filenames.
    *   Set paths and preprocessing options.
    *   If using OCR, ensure Tesseract is installed and `tesseract_cmd_path` is set if needed.
2.  **Run Acquisition Script:**
    ```bash
    python acquire_texts.py
    ```
    This will download the content from the URLs, perform initial HTML extraction with `trafilatura`, and save files to the raw directory (e.g., `data/textual/raw/`).
3.  **Run Preprocessing Script:**
    ```bash
    python preprocess_texts.py
    ```
    This will:
    *   Convert PDFs from the raw directory to text.
    *   Perform OCR if specified and configured.
    *   Clean all resulting `.txt` files.
    *   Identify language.
    *   Save cleaned text and language metadata to the processed directory (e.g., `data/textual/processed/`).

Check the log file for details on operations and any errors. Processed files will be plain text, ready for further NLP analysis.

## Notes on Extraction & OCR

*   **HTML Extraction:** `trafilatura` is effective for many news articles and blog posts. However, its success can vary depending on website structure. The raw HTML is also saved if deeper manual extraction is needed.
*   **PDF Conversion:** Text-based PDFs will be converted. For scanned/image-based PDFs, OCR is required.
*   **OCR Accuracy:** Tesseract's accuracy depends on image quality (DPI, noise, skew), font, and language. Preprocessing images before OCR (e.g., binarization, deskewing) can improve results but is not currently implemented in this basic pipeline. For high-accuracy OCR on challenging documents, commercial solutions or advanced open-source OCR engines might be necessary. This pipeline provides a basic integration point.
