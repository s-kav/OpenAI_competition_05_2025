# Data Acquisition and Preprocessing Workflows

This document details the initial data acquisition and preprocessing workflows for key data types identified in `PHASE_1_PLAN.md`. The focus is on programmatic access and leveraging open-source tools, primarily within a Python environment.

## 1. Satellite Imagery (e.g., Sentinel-2, Landsat)

Satellite imagery is crucial for identifying surface anomalies, vegetation patterns, and monitoring changes over time that might indicate archaeological sites.

### Acquisition

1.  **Define Area of Interest (AOI):**
    *   The primary AOI will be the Amazon basin region as specified by the competition guidelines. This will likely be provided as a GeoJSON file or a set of bounding box coordinates.
    *   For initial exploration or specific sub-regions, smaller AOIs can be defined using tools like [geojson.io](http://geojson.io/) or programmatically using libraries like `shapely` and `geopandas`.
    *   The AOI geometry will be used to query data providers. Ensure AOI is in WGS84 (EPSG:4326) for most APIs.

2.  **Select Data Sources & Programmatic Access:**
    *   **Sentinel-2:**
        *   **Library:** `sentinelsat` Python library.
        *   **Access:** Connect to the Copernicus Open Access Hub (SciHub - `https://apihub.copernicus.eu/apihub` - though reliability can vary) or alternative mirrors like PEPS from CNES (`https://peps.cnes.fr/resto/api/collections/S2ST`). Requires user credentials for the respective service.
        *   **Example Query Snippet (Python using `sentinelsat`):**
            ```python
            from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
            from datetime import date

            # api = SentinelAPI('user', 'password', 'https://apihub.copernicus.eu/apihub')
            api = SentinelAPI('your_peps_user', 'your_peps_password', 'https://peps.cnes.fr/resto/api/collections/S2ST')
            
            # Assuming AOI is defined in a GeoJSON file 'aoi.geojson'
            # footprint = geojson_to_wkt(read_geojson('aoi.geojson')) 
            
            # For a large area like the Amazon, a bounding box might be more practical initially
            # Example bounding box: (lon_min, lat_min, lon_max, lat_max)
            # amazon_bbox = (-75, -15, -45, 5) # Covers a large part of the Amazon
            # footprint = f"POLYGON(({amazon_bbox[0]} {amazon_bbox[1]}, {amazon_bbox[0]} {amazon_bbox[3]}, {amazon_bbox[2]} {amazon_bbox[3]}, {amazon_bbox[2]} {amazon_bbox[1]}, {amazon_bbox[0]} {amazon_bbox[1]}))"


            # products = api.query(footprint, 
            #                      date=('20230101', '20230331'), # Example date range
            #                      platformname='Sentinel-2',
            #                      producttype='S2MSI2A', # Level-2A for Surface Reflectance
            #                      cloudcoverpercentage=(0, 20))
            
            # products_gdf = api.to_geodataframe(products)
            # if not products_gdf.empty:
            #    api.download_all(products_gdf.index)
            ```
    *   **Landsat (Collections 2, Level-2):**
        *   **Libraries:** `pystac_client` to search STAC catalogs (e.g., AWS Open Data, Microsoft Planetary Computer), `usgs` package (requires M2M account setup for EarthExplorer API for some functionalities).
        *   **Access:** USGS EarthExplorer, AWS Open Data Program for Landsat, Microsoft Planetary Computer. These often provide STAC endpoints.
        *   **Example using `pystac_client` for AWS Landsat Collection 2 Level-2:**
            ```python
            from pystac_client import Client
            
            # catalog = Client.open("https://landsatlook.usgs.gov/stac-server") # USGS STAC (may change)
            catalog = Client.open("https://earth-search.aws.element84.com/v1") # Element 84 STAC for AWS data

            # Define AOI (geojson geometry or bbox [min_lon, min_lat, max_lon, max_lat])
            # aoi_geometry_geojson = {"type": "Polygon", "coordinates": [[[-75,-15],[-75,5],[-45,5],[-45,-15],[-75,-15]]]}
            # search = catalog.search(
            #     collections=["landsat-c2-l2"], # Landsat Collection 2 Level 2 (Surface Reflectance)
            #     intersects=aoi_geometry_geojson, # or bbox=amazon_bbox
            #     datetime="2023-01-01/2023-03-31",
            #     query={"eo:cloud_cover": {"lt": 20}} # lt for less than
            # )
            # items_dict = search.get_all_items_as_dict()
            # For downloading assets (bands) from items, use libraries like `stackstac` or direct HTTP requests via asset hrefs.
            ```

3.  **Image Selection Criteria:**
    *   **Date Range:** Prioritize recent imagery (last 1-5 years) for current land cover. Also acquire historical imagery (e.g., Landsat 5/7 spanning 1980s-2000s from Collection 2) to detect long-term changes. Dry season imagery (typically May-October, varies by specific Amazonian sub-region) is generally preferred.
    *   **Cloud Cover:** Aim for < 10-20% cloud cover *over the actual AOI within an image tile*. This may require iterating through query results and inspecting individual image footprints or quality masks if available via STAC properties.
    *   **Processing Level:** Strictly Sentinel-2 Level-2A (`S2MSI2A` or `L2A`) or Landsat Collection 2 Level-2 (e.g., `landsat_ot_c2_l2`). These are atmospherically corrected to Surface Reflectance.
    *   **Spatial Resolution:** Utilize the highest available native resolution bands (e.g., 10m for Sentinel-2 RGB & NIR; 30m for Landsat).

### Preprocessing

1.  **Atmospheric Correction Verification:**
    *   Double-check metadata to ensure products are indeed Surface Reflectance (SR). Level-2A (Sentinel-2) and Level-2 (Landsat C2) should be SR.
    *   If for some reason only Level-1C (Sentinel-2 Top-of-Atmosphere) or Level-1 (Landsat) are available, atmospheric correction is mandatory.
        *   Sentinel-2 L1C: `sen2cor` (ESA tool) or Python wrappers.
        *   Landsat L1: USGS ESPA service or libraries like `Py6S` (complex).
        *   Consider using Analysis Ready Data (ARD) if available from providers like `force` (Framework for Operational Radiometric Correction for Environmental monitoring).

2.  **Cloud Masking:**
    *   **Sentinel-2 (Level-2A):** Use the Scene Classification Layer (SCL) band. Values for cloud (usually 8=medium probability, 9=high probability, 10=thin cirrus) and cloud shadow (3) are key.
        *   **Libraries:** `rasterio` to read SCL and create masks. `xarray_sentinel` can simplify access.
    *   **Landsat (Collection 2, Level-2):** Use the Quality Assessment (QA_PIXEL) band. Specific bit flags indicate cloud, cloud shadow, cirrus.
        *   **Libraries:** `rasterio`, `xarray`. `earthpy` has helper functions. `eo-protocol` can help interpret QA bands.
    *   **Algorithms/Tools:**
        *   `s2cloudless` (Python library for Sentinel-2, uses ML).
        *   Fmask (Function of Mask) is a common algorithm, often integrated into processing frameworks or available as standalone tools.
    *   **Method:** Create a binary mask (e.g., 1 for clear, 0 for cloud/shadow/cirrus). Apply this mask to all relevant spectral bands, often by setting cloudy pixels to `NaN`.

3.  **Mosaicking:**
    *   **Purpose:** To combine multiple adjacent satellite image tiles to cover the entire AOI.
    *   **Tools/Libraries:**
        *   **GDAL:** `gdal_merge.py` (command-line) or `gdal.BuildVRT` (creates a virtual raster, efficient for many operations) followed by `gdal.Translate` (to create a physical mosaic).
        *   **Rasterio:** `rasterio.merge.merge` function.
        *   `xarray` with `rioxarray`: Can combine datasets using functions like `xr.open_mfdataset` (if files are structured correctly), `xr.concat`, or `xr.combine_by_coords` after aligning them. `stackstac` can also build data cubes from STAC items.
    *   **Considerations:** Feathering/Blending at seams, histogram matching (if images are from different conditions), order of operations.

4.  **Resampling (if combining different sensors or for standardization):**
    *   **Purpose:** To align pixel sizes (e.g., Sentinel-2 10m with Landsat 30m).
    *   **Tools/Libraries:**
        *   **GDAL:** `gdalwarp`.
        *   **Rasterio:** `rasterio.warp.reproject` using appropriate `Resampling` methods (e.g., `nearest` for categorical, `bilinear` or `cubic` for continuous data).
    *   **Caution:** Upsampling can imply false precision. Choose methods carefully.

5.  **Clipping to AOI:**
    *   **Purpose:** To reduce file sizes and focus analysis on the precise area of interest after mosaicking or for individual tiles.
    *   **Tools/Libraries:**
        *   **GDAL:** `gdalwarp -cutline aoi.geojson -crop_to_cutline ...`
        *   **Rasterio:** `rasterio.mask.mask` function.
        *   `rioxarray`: `rio.clip(aoi_geometries, crs=aoi_crs)` method.
    *   Ensure AOI geometry is in the same Coordinate Reference System (CRS) as the raster.

## 2. LiDAR Data

LiDAR data provides high-resolution elevation information, crucial for detecting subtle earthworks, paleochannels, and understanding micro-topography.

### Acquisition

1.  **Search and Discovery:**
    *   **OpenTopography:** ([https://opentopography.org/](https://opentopography.org/)) - Primary source for open LiDAR. Use map interface, search by keywords.
    *   **Academic Publications & Data Repositories:** Search Google Scholar, ResearchGate, Zenodo, tDAR (The Digital Archaeological Record) for papers/datasets related to Amazonian LiDAR.
    *   **National Data Portals:** INPE (Brazil), IGN (Peru), etc., may have data or links.
    *   **ICESat-2 Data:** Spaceborne LiDAR (photon-counting). Access via NASA NSIDC (Python library: `icepyx`). Useful for broader terrain/canopy height.

2.  **Download:**
    *   **OpenTopography:** Provides direct download (LAS/LAZ), often requires an account. May offer server-side processing (DEM generation, classification) for some datasets.
    *   **File Formats:**
        *   **LAS (LASer):** Standard binary format.
        *   **LAZ (LASzip):** Losslessly compressed LAS. Very common.
        *   **COPC (Cloud Optimized Point Cloud):** Newer format for efficient cloud streaming/querying. `pdal` supports COPC.

### Preprocessing

1.  **Format Conversion (LAZ to LAS, if necessary):**
    *   Most modern tools (PDAL, laspy) handle LAZ natively.
    *   **Tools:** `laszip` (command-line from LAStools or standalone). PDAL can convert:
        ```python
        # import pdal
        # pipeline_json = f"""{{ "pipeline": [ "{'input.laz'}", {{ "type": "writers.las", "filename": "{'output.las'}" }} ] }}"""
        # pipeline = pdal.Pipeline(pipeline_json)
        # pipeline.execute()
        ```

2.  **Filtering/Classification (Ground Point Classification):**
    *   **Purpose:** Separate ground returns (bare earth) from non-ground (vegetation, buildings). Essential for DTMs. Check LAS 'Classification' field (class 2 is usually ground).
    *   **If not classified or needs refinement:**
    *   **Tools/Libraries:**
        *   **PDAL:** `filters.smrf` (Simple Morphological Filter), `filters.pmf` (Progressive Morphological Filter), `filters.csf` (Cloth Simulation Filter).
            ```python
            # Example PDAL SMRF JSON snippet for a pipeline
            # { "type": "filters.smrf", "scalar": 1.2, "slope": 0.2, "threshold": 0.45, "window": 18.0 },
            # { "type": "filters.range", "limits": "Classification[2:2]" } # To keep only ground points
            ```
        *   **LAStools:** `lasground` (some parts free for non-commercial use).
        *   **CloudCompare:** Open-source GUI/CLI, plugins like CANUPO.
        *   **Python:** `pyfor`, `lidar` package. `whiteboxtools` (Python frontend for WhiteboxTools) has classification tools.
    *   **Verification:** Visual inspection of classified point clouds (e.g., color by class in CloudCompare, QGIS with `lastools` plugin).

3.  **Generation of Digital Terrain Models (DTMs):**
    *   **Purpose:** Create raster grids representing bare-earth elevation.
    *   **Tools/Libraries:**
        *   **PDAL:** `writers.gdal` to create rasters using interpolation (e.g., `mean`, `idw`, `nearest`).
        *   **GDAL:** `gdal_grid` (from XYZ), `gdal_rasterize` (if points are on a grid).
        *   **Python:** `whitebox.Runner.lidar_tin_gridding()`, `scipy.interpolate.griddata`. `Relief Visualization Toolbox (RVT)` (standalone, but callable from Python).
        *   **GIS Software:** QGIS, ArcGIS, SAGA GIS, GRASS GIS.

4.  **Visualization Techniques for Archaeological Features (applied to DTMs):**
    *   **Purpose:** Enhance subtle topographic features.
    *   **Techniques & Tools (GDAL, WhiteboxTools, RVT, QGIS/GRASS/SAGA GIS):**
        *   **Hillshade:** (GDAL: `gdaldem hillshade`, WhiteboxTools: `Hillshade`)
        *   **Multi-directional Hillshade:** Combine several hillshades.
        *   **Slope:** (GDAL: `gdaldem slope`, WhiteboxTools: `Slope`)
        *   **Sky-View Factor (SVF) / Openness:** (RVT, SAGA GIS, WhiteboxTools: `SkyViewFactor`, `OpennessPositiveNegative`) - excellent for small depressions/mounds.
        *   **Local Relief Model (LRM) / Trend-Removed DEM:** (SAGA GIS, WhiteboxTools: `RemoveTrend`, custom Python scripts).
        *   **Sky-Illumination:** (RVT)
    *   **Python Libraries:** `RichDEM` for terrain analysis.

## 3. Textual Data

Historical texts, academic papers, and (with ethical protocols) oral histories.

### Acquisition

1.  **Downloading Texts:**
    *   **Direct Download:** Project Gutenberg, Internet Archive, HathiTrust (public domain). Use `requests` in Python.
        ```python
        # import requests
        # url = "url_to_txt_or_pdf_file"
        # response = requests.get(url, stream=True)
        # with open("document.ext", "wb") as f: # 'wb' for binary (PDF)
        #     for chunk in response.iter_content(chunk_size=8192):
        #         f.write(chunk)
        ```
    *   **Web Scraping (Ethical & Respectful):**
        *   **Libraries:** `requests`, `BeautifulSoup4` or `lxml` (parsing), `trafilatura` (main content extraction).
        *   **Process:** Check `robots.txt`, Terms of Service. Implement delays (`time.sleep()`), use User-Agents. `requests-cache` for caching.
    *   **APIs:** Europeana, HathiTrust, DPLA, CORE UK. Preferred over scraping.

2.  **Handling Different Formats:** PDF, TXT, HTML, EPUB, DOCX, ODT.

### Preprocessing

1.  **Conversion to Plain Text:**
    *   **PDFs:**
        *   Text-based: `PyPDF2`, `pdfminer.six`, `pdftotext` (from `poppler-utils`).
            ```python
            # from pdfminer.high_level import extract_text
            # text = extract_text("document.pdf")
            ```
        *   Image-based/Scanned: Require OCR (see step 4).
    *   **HTML:** `BeautifulSoup4` (`.get_text()`), `html2text`, `trafilatura`.
    *   **EPUB:** `EbookLib` (Python) - extract HTML items, then parse.
    *   **DOCX:** `python-docx`. **ODT:** `odtpy`.

2.  **Text Cleaning:**
    *   **Purpose:** Remove noise, standardize for NLP. Iterative.
    *   **Steps:** Remove boilerplate (headers, footers, page numbers). Normalize Unicode (`unicodedata.normalize`). Remove irrelevant special characters. Normalize whitespace. Handle hyphenation (`pyphen`). Remove ligatures.
    *   **Libraries:** `re` (regex), `ftfy` (Unicode fixing), `cleantext`.

3.  **Language Identification and Translation:**
    *   **Identification:** `langdetect`, `langid`, `fastText`.
    *   **Translation (if necessary, e.g., to English for LLMs):**
        *   **Strategy:** Analyze in original language if possible. Translate if models are better in target language or for combining sources.
        *   **Tools:** OpenAI Models, `deep-translator` (wraps Google, DeepL), Hugging Face `MarianMT` models.
        *   **Caution:** Translation can lose nuance. Preserve original. For critical texts, consult experts.

4.  **Optical Character Recognition (OCR):**
    *   **Purpose:** Convert scanned documents/images to text.
    *   **Tool:** **Tesseract OCR**
        *   **Python Wrappers:** `pytesseract`, `tesserocr`.
            ```python
            # import pytesseract
            # from PIL import Image
            # # Requires Tesseract installed and in PATH, and language data
            # text = pytesseract.image_to_string(Image.open('scanned_page.png'), lang='eng+por+spa') # Add relevant languages
            ```
    *   **Preprocessing for OCR (CRUCIAL):** Image binarization (adaptive thresholding), noise removal, deskewing, DPI upscaling (target 300-600 DPI).
        *   **Libraries:** OpenCV (`cv2`), Pillow (`PIL`), `scikit-image`, `Leptonica`.
    *   **Postprocessing OCR:** Spell checking (`pyspellchecker`, `hunspell`), contextual error correction (LLMs can help here).
    *   **Quality Checks:** Manual spot-checking, automated metrics (CER/WER if ground truth exists).

This document outlines the acquisition and preprocessing workflows. Actual implementation will require iterative refinement and robust quality control for each step.
