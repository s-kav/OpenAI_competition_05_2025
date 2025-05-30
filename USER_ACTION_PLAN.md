# User Action Plan: Applying the AI-Driven Archaeological Survey Framework

## 0. Introduction

**Purpose:** This document provides a step-by-step guide for users who wish to apply the "Unveiling Traces of the Past" project framework to their own Area of Interest (AOI) within the Amazon biome and with their own sourced data. It aims to bridge the gap between the developed pipelines and methodologies and their practical application for new archaeological prospection efforts.

**Project Overview:** Before proceeding, users are strongly encouraged to familiarize themselves with the overall project structure, methodologies, and findings by reviewing:
*   The main project `README.md` located in the root of the repository (`OpenAI_LostCityZ_AmazonArchaeology/README.md`).
*   The `OpenAI_LostCityZ_AmazonArchaeology/reports/FINAL_REPORT.md` for a comprehensive understanding of the project's phases, tools, and example outputs.

This plan assumes you have access to the complete project repository and are working from within the `OpenAI_LostCityZ_AmazonArchaeology/` directory (i.e., this file is at the root of your project).

## 1. Setting Up Your Environment

To successfully run this project's pipelines and notebooks, you need to set up your computational environment correctly.

1.  **Clone the Repository (if not already done):**
    *   Obtain a copy of the project code on your local machine.
    *   Example Git command:
        ```bash
        git clone [URL_to_this_project_repository] OpenAI_LostCityZ_AmazonArchaeology
        cd OpenAI_LostCityZ_AmazonArchaeology
        ```

2.  **Install Python Dependencies:**
    *   It is highly recommended to use a virtual environment (e.g., Conda or Python's `venv`) to manage project dependencies.
    *   **Using Conda (Recommended):**
        ```bash
        conda env create -f environment.yml
        conda activate amazon_archaeology_env # Or the environment name defined in the yml
        ```
    *   **Using pip with `venv`:**
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # On Windows: .venv\Scripts\activate
        pip install -r requirements.txt
        ```
    *   The `environment.yml` (for Conda) and `requirements.txt` (for pip) are provided in the root directory of the repository.

3.  **Install System Dependencies:**
    *   Several geospatial libraries require system-level installations. Refer to their official installation guides for platform-specific instructions.
        *   **GDAL:** Essential for `rasterio` and `geopandas`. (Often easiest via Conda: `conda install -c conda-forge gdal`)
        *   **PDAL:** For LiDAR processing. (Often easiest via Conda: `conda install -c conda-forge pdal python-pdal`)
        *   **Sen2Cor (Optional):** Only required if you intend to process Sentinel-2 Level-1C data to Level-2A. This project's scripts primarily target direct use of Level-2A data. If needed, download from ESA STEP website and follow their installation guide. Note the path to the `L2A_Process` script.
        *   **Tesseract OCR Engine (Optional):** Only required if you need to perform OCR on image-based PDFs.
            *   Install Tesseract OCR: See `scripts/text_pipeline/README.md` (located at `OpenAI_LostCityZ_AmazonArchaeology/scripts/text_pipeline/README.md`) for links and basic OS-specific commands.
            *   Install language packs for Tesseract (e.g., English, Portuguese, Spanish).
        *   **Poppler Utilities (for `pdf2image` with PDF OCR):** If performing OCR on PDFs, `pdf2image` (a Python library used in the text pipeline) requires Poppler.
            *   Linux (Ubuntu/Debian): `sudo apt-get install poppler-utils`
            *   macOS: `brew install poppler`
            *   Windows: Requires downloading Poppler binaries and adding to PATH. See `pdf2image` documentation.

4.  **Set Up OpenAI API Key:**
    *   Required for functionalities in `notebooks/textual_eda_openai.ipynb` and conceptual plausibility assessment in `notebooks/piz_identification_scoring.ipynb`.
    *   **Recommended Method:** Set it as an environment variable named `OPENAI_API_KEY`.
        ```bash
        export OPENAI_API_KEY='sk-YourActualOpenAIKeyHere' 
        ```
        (Add this to your shell's startup file like `.bashrc` or `.zshrc` for persistence, or set it for your current session).
    *   The scripts and notebooks are configured to look for this environment variable. **Do not hardcode your key into scripts or notebooks.**

## 2. Defining Your Area of Interest (AOI)

1.  **Select an AOI:**
    *   Choose a specific area within the Amazon biome that you wish to investigate.
    *   Consider data availability (LiDAR, recent Sentinel-2 coverage) for your chosen region.
    *   Start with a relatively small AOI (e.g., 10km x 10km or 20km x 20km) to test the entire pipeline and manage data volumes before scaling up.

2.  **Create a GeoJSON File for Your AOI:**
    *   The project uses a GeoJSON file to define the precise boundaries of your AOI for data processing and analysis.
    *   **How to Create:**
        *   **Using GIS Software (e.g., QGIS - Recommended):**
            1.  Create a new vector layer (polygon).
            2.  Draw your AOI polygon.
            3.  Ensure the layer's Coordinate Reference System (CRS) is **EPSG:4326 (WGS 84 geographic coordinates)**.
            4.  Save the layer as a GeoJSON file (e.g., `my_aoi.geojson`).
        *   **Using Online Tools:** Tools like [geojson.io](http://geojson.io/) allow you to draw a polygon on a map and save it as GeoJSON. Ensure the output is a valid GeoJSON Polygon or MultiPolygon.
    *   **File Naming and Placement:**
        *   Name your file descriptively, e.g., `my_specific_region_aoi.geojson`.
        *   Place this file into the `data/aoi/` directory (i.e., `OpenAI_LostCityZ_AmazonArchaeology/data/aoi/`).
        *   For initial testing, you can replace the placeholder `data/aoi/aoi_boundary.geojson` with your file or update the path in `config/config.ini`.

## 3. Configuring the Project (`config/config.ini`)

The central configuration file for all pipelines is `config/config.ini` (i.e., `OpenAI_LostCityZ_AmazonArchaeology/config/config.ini`). You **must** update this file to reflect your chosen AOI, data sources, and API credentials.

1.  **`[DEFAULT]` Section:**
    *   `api_user` & `api_password`: Enter your credentials for Copernicus Open Access Hub (SciHub) or preferably PEPS (CNES) for Sentinel-2 data acquisition. Register for an account if you don't have one.
    *   `api_url`: Ensure this points to the correct API endpoint (default is PEPS for Sentinel-2).
    *   `aoi_bbox`: You can define a simple rectangular AOI here (lon_min, lat_min, lon_max, lat_max in WGS84 decimal degrees). **However, using `aoi_geojson_path` is recommended for more precise AOIs.** If `aoi_geojson_path` is set and valid, it will override `aoi_bbox`.
    *   `aoi_geojson_path`: **Crucial.** Update this to the path of your AOI GeoJSON file. This path should be relative to the project root directory (e.g., `data/aoi/my_specific_region_aoi.geojson`).
    *   `start_date`, `end_date`: Define the date range (YYYYMMDD format) for Sentinel-2 image acquisition for your AOI.
    *   `cloud_cover_percentage`: Maximum cloud cover allowed for Sentinel-2 tiles (e.g., 10-20%).
    *   Paths like `log_dir`, `base_raw_data_dir`, `base_processed_data_dir`: These are configured as relative paths (e.g., `../../logs`, `../../data`) which are interpreted by the scripts from their locations to point to the project's root `logs/` and `data/` directories. Default values should generally work with the provided structure.
    *   Log file names (`satellite_log_file_name`, etc.): Can be customized if desired.

2.  **`[SEN2COR]` Section (Optional):**
    *   `sen2cor_path`: Only needed if you set `product_type = S2MSI1C` in `[DEFAULT]` and want to process Sentinel-2 Level-1C data. Provide the full path to your Sen2Cor `L2A_Process` script.

3.  **`[PREPROCESSING]` Section (Sentinel-2):**
    *   `target_resolution`: Target resolution for processed Sentinel-2 bands (e.g., 10 or 20 meters).
    *   `output_bands`: Comma-separated list of Sentinel-2 bands to include in processed files (e.g., `B02,B03,B04,B08`).
    *   `scl_mask_classes`: SCL classes to be masked as cloud/shadow.

4.  **`[LIDAR]` Section:**
    *   `lidar_data_urls`: **User Action Required.** You must populate this with direct download URLs for any LAS or LAZ LiDAR files you find that cover your AOI. Each URL should be on a new line. Use resources like OpenTopography, university archives, or national data portals to find LiDAR data.
    *   `lidar_raw_suffix`, `lidar_processed_suffix`: Define subdirectories for LiDAR data. Defaults should work.
    *   `dtm_resolution`, `dtm_interpolation_method`: Parameters for DTM generation via PDAL.
    *   `target_projected_crs`: **Very Important.** Specify an appropriate projected CRS (e.g., a UTM zone like `EPSG:31980`) for your AOI. PDAL processing (ground classification, DTM generation) works best with projected coordinates. You *must* change the default `EPSG:31980` if your AOI is not in UTM Zone 20N (SIRGAS 2000 datum), or another suitable projected CRS for your region.
    *   `ground_classification_pipeline_json`, `dtm_generation_pipeline_json`: These are PDAL pipeline templates. The `TARGET_PROJECTED_CRS_PLACEHOLDER` will be automatically replaced by the `target_projected_crs` value. You may need to adjust filter parameters (e.g., SMRF settings) within these JSON strings based on your LiDAR data characteristics, but start with the defaults.
    *   Hillshade parameters: `hillshade_azimuth`, `hillshade_altitude`, etc.

5.  **`[TextualData]` Section:**
    *   `text_data_sources`: **User Action Required.** Populate this list with URLs of textual documents relevant to your AOI (e.g., historical accounts, ethnographic studies, archaeological papers). Format: `URL | TYPE (Optional: TXT, HTML, PDF, PDF_OCR) | Custom_Output_Filename (Optional)`. Find sources in digital libraries, archives, and academic databases.
    *   Path suffixes: Defaults should work.
    *   Processing settings: `clean_text_to_lowercase`, `custom_remove_patterns_json` (for text cleaning).
    *   `ocr_languages`, `tesseract_cmd_path`, `pdf_extraction_method`, `pdf_ocr_dpi`: Configure these if you plan to use OCR for PDFs. Ensure Tesseract is installed and the path is correct if not in system PATH.

## 4. Data Acquisition and Preprocessing (Running the Scripts)

Once your environment is set up and `config/config.ini` is configured for your AOI and data sources, run the Python scripts located in the `scripts/` subdirectories. It's generally recommended to run them from the project's root directory (e.g., `python scripts/satellite_pipeline/acquire_sentinel2.py`).

**Execution Order:**

1.  **Sentinel-2 Satellite Imagery:**
    *   `python scripts/satellite_pipeline/acquire_sentinel2.py`: Downloads Sentinel-2 products based on your AOI and parameters in `config.ini`.
    *   `python scripts/satellite_pipeline/preprocess_sentinel2.py`: Processes the downloaded Sentinel-2 data (cloud masking, band selection, clipping, etc.). Output goes to `data/processed/sentinel2/`.

2.  **LiDAR Data:**
    *   `python scripts/lidar_pipeline/acquire_lidar.py`: Downloads LiDAR files from the URLs you provided in `config.ini`.
    *   `python scripts/lidar_pipeline/preprocess_lidar.py`: Processes downloaded LiDAR (LAZ to LAS, ground classification, DTM/hillshade generation, clipping). Output goes to `data/processed/lidar/`.

3.  **Textual Data:**
    *   `python scripts/text_pipeline/acquire_texts.py`: Downloads textual data from URLs in `config.ini`, performs initial HTML extraction. Raw files (HTML, PDF, TXT) and initially extracted TXT from HTML go to `data/raw/textual/`.
    *   `python scripts/text_pipeline/preprocess_texts.py`: Converts PDFs to text (native or OCR), cleans all text files, identifies language. Output goes to `data/processed/textual/`.

*   **Check Logs:** Monitor progress and check for errors in the log files created in the `logs/` directory (e.g., `satellite_pipeline.log`, `lidar_pipeline.log`, `text_pipeline.log`).
*   **Start Small:** For your first run, configure a very small AOI and a limited number of data sources (e.g., one Sentinel-2 scene, one small LiDAR file, a few text URLs) to ensure the pipeline runs correctly before attempting large-scale processing.

## 5. Exploratory Data Analysis (Running the Notebooks)

After successfully acquiring and preprocessing data for your AOI, you can perform EDA using the Jupyter Notebooks in the `notebooks/` directory. Launch Jupyter Lab from your project root directory (`OpenAI_LostCityZ_AmazonArchaeology/`).

1.  **Run `notebooks/lidar_eda.ipynb`:**
    *   This notebook will load processed DTMs and hillshades from `data/processed/lidar/` for your AOI.
    *   It generates various visualizations (DTM, multi-azimuth hillshades, slope, aspect, contours).
    *   Analyze these visualizations for topographic anomalies. Document your observations directly in the notebook or in separate notes, saving key images to `eda_outputs/lidar/`.

2.  **Run `notebooks/satellite_eda.ipynb`:**
    *   Loads processed multi-band Sentinel-2 GeoTIFFs from `data/processed/sentinel2/`.
    *   Generates true/false color composites and spectral indices (NDVI, NDWI, BSI, etc.).
    *   Analyze for spectral anomalies, unusual vegetation patterns, or soil marks. Document observations and save images to `eda_outputs/satellite/`.

3.  **Run `notebooks/textual_eda_openai.ipynb`:**
    *   Loads processed text files from `data/processed/textual/`.
    *   Demonstrates using the OpenAI API for NER, conceptual topic modeling, relationship extraction, and geocoding assistance.
    *   **Ensure your `OPENAI_API_KEY` is set as an environment variable.**
    *   Analyze the AI-generated outputs. Document entities, themes, and potential geographic clues relevant to your AOI. Store relevant JSON outputs or summaries in `eda_outputs/textual/`.

*   **Notebook Configuration:** The notebooks are designed to load paths from `config/config.ini`. The `CONFIG_FILE_PATH` variable at the top of each notebook is set to `../config/config.ini` (assuming notebooks are run from the `notebooks/` directory, this correctly points to `config/config.ini` at the project root).
*   **Adapt and Observe:** The primary purpose of this step is for *you* to explore *your* data. Modify code cells as needed to focus on specific features or sub-regions within your AOI. Save your modified notebooks if you wish to keep a record of your specific analyses.

## 6. Identifying and Scoring Potential Interest Zones (PIZs)

This step uses the `notebooks/piz_identification_scoring.ipynb` notebook to integrate your EDA findings and identify high-potential areas.

1.  **Adapt `piz_identification_scoring.ipynb`:**
    *   **Crucial Step:** The section "2. Load (Placeholder) EDA Outputs" currently uses manually curated placeholder data. You **must modify this section** to load *your actual anomaly data* identified during your EDA (Step 5).
        *   This might involve reading GeoJSON files you created to save anomaly locations, or loading CSVs with coordinates and attributes of features you noted during your EDA.
        *   Ensure your anomaly GeoDataFrames have attributes that match what the heuristic scoring function expects (e.g., `lidar_clarity`, `satellite_significance`, `textual_reliability`, and feature type descriptions).
    *   Review and adjust the `BUFFER_DISTANCE_METERS` if needed for your AOI's scale or feature types.
    *   Review and tune the heuristic scoring `weights` in Section 4 of the notebook if you have specific reasons to prioritize certain data types or feature characteristics for your AOI.

2.  **Run the Notebook:** Execute the cells sequentially. The notebook will:
    *   Define PIZs based on the spatial overlap/proximity of your input anomalies.
    *   Calculate heuristic scores for these PIZs.
    *   Generate a ranked list of PIZs (saved to `eda_outputs/piz/`).
    *   Visualize the PIZs on a map.
    *   Provide example prompts for OpenAI plausibility assessment for your top-scoring PIZs.

## 7. Verification and Evidence Compilation

Once you have a ranked list of PIZs for your AOI:

1.  **Refer to Verification Procedures:** Consult `project_documentation/PIZ_VERIFICATION_PROCEDURES.md`. This document details several methods to increase confidence in your PIZs (e.g., detailed cross-data re-analysis, comparative analysis with known sites from literature, historical map overlays).
2.  **Apply Verification Methods:** Select and apply at least two distinct verification methods to your top N PIZs.
3.  **Compile Evidence Dossiers:** For each verified top PIZ, compile a detailed "Site Dossier" using the template and guidelines in `project_documentation/EVIDENCE_COMPILATION_INSIGHT_GENERATION_GUIDELINES.md`.
    *   This includes summarizing LiDAR, satellite, and textual evidence specific to the PIZ.
    *   Document the verification findings.
    *   Use the OpenAI prompt strategies (from the guidelines and demonstrated in `piz_identification_scoring.ipynb`) to generate synthesized narratives and historical insights for your PIZ, based on *your compiled evidence*.

## 8. Iteration and Further Work

Archaeological prospection is an iterative process.
*   Based on your initial PIZ results and verification, you might need to:
    *   Refine your AOI (expand or focus on sub-regions).
    *   Search for additional or different types of data.
    *   Adjust parameters in the preprocessing scripts or scoring notebook.
    *   Conduct more detailed EDA on specific high-potential zones.
*   Consider how the tools and methodologies developed in this project could be further enhanced or adapted for different archaeological questions or environmental contexts.

This action plan provides a comprehensive roadmap for applying this project's framework. Success will depend on careful configuration, thorough data sourcing for your specific AOI, and critical interpretation of results at each stage. Good luck with your archaeological discoveries!
