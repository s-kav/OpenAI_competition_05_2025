# LiDAR Data Processing Pipeline

This pipeline provides scripts to acquire (via direct URLs) and preprocess LiDAR data (LAZ/LAS files) to generate Digital Terrain Models (DTMs) and hillshades.

## Features

*   **Data Acquisition (`acquire_lidar.py`):**
    *   Downloads LiDAR files from a list of URLs specified in the configuration.
    *   Stores downloaded files in a structured raw data directory.
    *   Logs download activities and handles errors.
*   **Data Preprocessing (`preprocess_lidar.py`):**
    *   Converts LAZ to LAS if necessary (using `laspy` or `pdal`).
    *   Performs ground point classification using PDAL pipelines (e.g., SMRF or PMF).
    *   Generates DTMs (GeoTIFF format) from ground points using PDAL.
    *   Generates hillshade rasters from DTMs using GDAL (via Rasterio).
    *   Clips DTMs and hillshades to a defined Area of Interest (AOI).
    *   Logs all processing steps.

## Setup

### 1. Dependencies

Install the required Python libraries:

```bash
pip install pdal rasterio geopandas shapely requests laspy # laspy for LAZ->LAS if not using PDAL for it
```

**Additionally, you need to install PDAL and GDAL:**

*   **PDAL:** Installation instructions vary by OS. Refer to the official PDAL documentation: [https://pdal.io/en/latest/installation.html](https://pdal.io/en/latest/installation.html)
    *   For Conda users (recommended): `conda install -c conda-forge pdal python-pdal gdal`
*   **GDAL:** If not installed via Conda with PDAL, ensure GDAL command-line tools are available and that the Python `rasterio` library can find them. `pip install gdal` might work on some systems, but Conda is generally more reliable for GDAL.
*   **Laszip (Optional if using `laspy` or PDAL for LAZ):** If you need to use the `laszip` command-line tool directly, download it from [https://laszip.org/](https://laszip.org/) and ensure it's in your system PATH.

### 2. Configuration File

Update your main `config.ini` file (or create a new one if this is a standalone pipeline, but this guide assumes adding to an existing one from a previous satellite pipeline setup) with a `[LIDAR]` section.

Example `config.ini` additions:

```ini
[DEFAULT]
# ... (existing DEFAULT settings like log_dir, log_file_name, aoi_bbox, aoi_geojson_path)
# Ensure AOI is defined here if it's shared with other pipelines

[LIDAR]
# List of direct download URLs for LiDAR files (LAZ or LAS)
# Separate multiple URLs with a newline
lidar_data_urls =
    https://example.com/path/to/your/lidar_data_1.laz
    # https://example.com/path/to/your/lidar_data_2.las

# Output Directories (relative to scripts/lidar_pipeline/ or absolute)
lidar_raw_dir = ../../data/lidar/raw
lidar_processed_dir = ../../data/lidar/processed # For LAS, DTMs, Hillshades

# DTM Generation Parameters
dtm_resolution = 1.0 # Output resolution for DTM in meters
dtm_interpolation_method = mean # PDAL writer.gdal method: mean, idw, min, max, etc.

# PDAL Pipeline for Ground Classification (SMRF example)
# This can be a JSON string directly in the config or a path to a .json file
# Ensure paths within the JSON (input.las, output_ground.las) are placeholders;
# the script will substitute them.
ground_classification_pipeline_json = {
    "pipeline": [
        {
            "type": "readers.las",
            "filename": "INPUT_FILE_PLACEHOLDER"
        },
        {
            "type": "filters.reprojection",
            "out_srs": "EPSG:YOUR_PROJECTED_CRS" # Important: Reproject to a suitable projected CRS for geometric operations
        },
        {
            "type": "filters.smrf",
            "scalar": 1.2,
            "slope": 0.15,
            "threshold": 0.45,
            "window": 18.0,
            "ignore": "Classification[7:7]" # Ignore noise points if already classified
        },
        {
            "type": "filters.range",
            "limits": "Classification[2:2]" # Keep only ground points (PDAL class 2)
        },
        {
            "type": "writers.las",
            "filename": "OUTPUT_GROUND_FILE_PLACEHOLDER"
        }
    ]
}
# Example for EPSG:YOUR_PROJECTED_CRS:
# If your AOI is in Brazil near Manaus (approx UTM Zone 20N or 21N, or SIRGAS 2000 based UTM)
# e.g., "EPSG:31980" for UTM Zone 20N with SIRGAS 2000 datum.
# Choose a CRS appropriate for your specific AOI to minimize distortion.

# PDAL Pipeline for DTM Generation
dtm_generation_pipeline_json = {
    "pipeline": [
        {
            "type": "readers.las",
            "filename": "INPUT_GROUND_POINTS_PLACEHOLDER"
        },
        {
            "type": "writers.gdal",
            "filename": "OUTPUT_DTM_FILE_PLACEHOLDER",
            "gdaldriver": "GTiff",
            "output_type": "mean", # Set from dtm_interpolation_method
            "resolution": 1.0 # Set from dtm_resolution
        }
    ]
}

# Hillshade Parameters
hillshade_azimuth = 315
hillshade_altitude = 45
hillshade_z_factor = 1 # Vertical exaggeration
```

Ensure the output directories exist, or the scripts have permission to create them. You might need to create them manually:
`mkdir -p ../../data/lidar/raw ../../data/lidar/processed` (adjust path based on your `config.ini` location if it's not in `scripts/lidar_pipeline/`).

### 3. Projected Coordinate System (CRS) for PDAL

**Critical:** For ground classification and DTM generation, LiDAR data should ideally be in a projected CRS suitable for the AOI, not a geographic CRS (like WGS84 EPSG:4326). The example `ground_classification_pipeline_json` includes a `filters.reprojection` stage. **You MUST update `EPSG:YOUR_PROJECTED_CRS`** in the config with an appropriate EPSG code for your data's location. If your input data is already in a suitable projected CRS, you might be able to remove or adjust this reprojection step, but it's good practice for consistency.

## Usage

1.  **Configure `config.ini`:**
    *   Add/update the `[LIDAR]` section.
    *   Provide direct download URLs for your LAZ/LAS files.
    *   Ensure your AOI is defined (e.g., `aoi_bbox` or `aoi_geojson_path` in `[DEFAULT]`).
    *   **Crucially, set `EPSG:YOUR_PROJECTED_CRS` in `ground_classification_pipeline_json`.**
    *   Adjust DTM resolution, interpolation method, and PDAL pipeline parameters as needed.
2.  **Run Acquisition Script:**
    ```bash
    python acquire_lidar.py
    ```
    This will download the LiDAR files to the `lidar_raw_dir`.
3.  **Run Preprocessing Script:**
    ```bash
    python preprocess_lidar.py
    ```
    This will:
    *   Convert LAZ to LAS (if needed).
    *   Classify ground points.
    *   Generate DTMs.
    *   Generate hillshades.
    *   Clip outputs to AOI.
    *   Save results in `lidar_processed_dir`.

Check the main log file (e.g., `logs/satellite_pipeline.log` or a new `lidar_pipeline.log` if you configure it) for details on the operations.

## PDAL Pipelines

The preprocessing script uses PDAL for ground classification and DTM generation. The JSON configurations for these pipelines are included in the `config.ini` or can be paths to separate JSON files.

*   **Ground Classification:** The example uses `filters.smrf` (Simple Morphological Filter). Other options include `filters.pmf` (Progressive Morphological Filter) or `filters.csf` (Cloth Simulation Filter). Parameters for these filters need to be tuned based on terrain and vegetation characteristics.
*   **DTM Generation:** Uses `writers.gdal` to create a GeoTIFF raster. Resolution and interpolation method are configurable.

It's highly recommended to experiment with PDAL pipeline parameters using a small subset of your data to achieve optimal results before processing large datasets. Tools like `pdal info` and visualization in CloudCompare or QGIS are essential for this.
