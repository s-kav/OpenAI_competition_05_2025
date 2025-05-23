# Sentinel-2 Satellite Imagery Processing Pipeline

This pipeline provides scripts to acquire and preprocess Sentinel-2 satellite imagery for a defined Area of Interest (AOI).

## Features

*   **Data Acquisition (`acquire_sentinel2.py`):**
    *   Downloads Sentinel-2 (Level-2A preferred) products using the `sentinelsat` library.
    *   Filters by date range, maximum cloud cover, and AOI.
    *   Logs download activities.
    *   Handles download errors gracefully.
*   **Data Preprocessing (`preprocess_sentinel2.py`):**
    *   Performs cloud masking using quality bands (SCL from Level-2A products).
    *   Clips imagery to the exact AOI.
    *   Saves processed imagery in GeoTIFF format.
    *   Logs processing steps.
    *   (Future/Optional: Integration or guidance for `sen2cor` if Level-1C data is used).

## Setup

### 1. Dependencies

Install the required Python libraries:

```bash
pip install sentinelsat rasterio geopandas shapely s2cloudless # Add other necessary libraries
```

(Note: `s2cloudless` is listed as an option, primary implementation will use L2A SCL bands first).

### 2. Configuration File

Create a `config.ini` file in this directory (`scripts/satellite_pipeline/`) with the following structure:

```ini
[DEFAULT]
# Define your Copernicus Open Access Hub (SciHub) or PEPS credentials
# PEPS (https://peps.cnes.fr) is often more reliable
# Register at https://peps.cnes.fr/register
#api_user = your_username
#api_password = your_password
#api_url = https://peps.cnes.fr/resto/api/collections/S2ST # PEPS S2ST endpoint for Sentinel-2

# Define your Area of Interest (AOI)
# Option 1: Bounding Box (lon_min, lat_min, lon_max, lat_max)
# Ensure coordinates are in WGS84 (EPSG:4326)
# Example: A small area in the Amazon
aoi_bbox = -60.0, -3.0, -59.5, -2.5 # Manaus region, Brazil (approx. 55x55km)

# Option 2: Path to a GeoJSON file defining the AOI
# aoi_geojson_path = path/to/your/aoi.geojson

# Data Acquisition Parameters
start_date = 20230101
end_date = 20230331
cloud_cover_percentage = 10 # Maximum cloud cover percentage for a tile

# Output Directories
raw_data_dir = ./data/sentinel2/raw
processed_data_dir = ./data/sentinel2/processed
log_file = ./logs/satellite_pipeline.log

[SEN2COR]
# Optional: Path to Sen2Cor L2A_Process.bat or L2A_Process.sh script
# sen2cor_path = /path/to/Sen2Cor-X.Y.Z-Linux64/bin/L2A_Process
# Required if processing Level-1C products to Level-2A.
# If using Level-2A products directly, this can be ignored.
```

Ensure the output directories (`./data/sentinel2/raw`, `./data/sentinel2/processed`) and log directory (`./logs/`) exist or the scripts have permission to create them. You might need to create them manually:
`mkdir -p ./data/sentinel2/raw ./data/sentinel2/processed ./logs`

### 3. Sen2Cor (Optional - If processing Level-1C data)

If you plan to download Sentinel-2 Level-1C data and process it to Level-2A (surface reflectance), you will need to install Sen2Cor from ESA.

1.  **Download Sen2Cor:** Visit the ESA Sen2Cor download page ([https://step.esa.int/main/snap-supported-plugins/sen2cor/](https://step.esa.int/main/snap-supported-plugins/sen2cor/)) and download the version appropriate for your operating system.
2.  **Installation:** Follow the installation instructions provided with the download. This usually involves extracting the archive and potentially setting some environment variables (like `SEN2COR_HOME`, `SEN2COR_BIN`).
3.  **Configuration:** Note the path to the `L2A_Process` script (e.g., `L2A_Process.bat` on Windows, `L2A_Process.sh` on Linux/macOS) and update it in the `config.ini` file if you intend to use the `preprocess_sentinel2.py` script to call Sen2Cor.

**Note:** This pipeline primarily targets direct download and use of **Level-2A** products, which are already atmospherically corrected. Sen2Cor is only needed if you explicitly choose to work with Level-1C data.

## Usage

1.  **Configure `config.ini`:** Fill in your API credentials, define your AOI, date range, and other parameters.
2.  **Run Acquisition Script:**
    ```bash
    python acquire_sentinel2.py
    ```
    This will download Sentinel-2 products matching your criteria to the `raw_data_dir`.
3.  **Run Preprocessing Script:**
    ```bash
    python preprocess_sentinel2.py
    ```
    This will process the raw data (cloud mask, clip) and save the results in the `processed_data_dir`.

Check the `satellite_pipeline.log` file in the `logs` directory for details on the operations.
