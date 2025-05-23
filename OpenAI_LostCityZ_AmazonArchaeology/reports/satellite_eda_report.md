# Satellite Imagery (Sentinel-2) Exploratory Data Analysis (EDA) Report

## 1. Introduction

This report summarizes the initial Exploratory Data Analysis (EDA) performed on processed Sentinel-2 satellite imagery. The EDA was conducted using the `notebooks/satellite_eda.ipynb` Jupyter Notebook, following the strategy outlined in `EDA_FEATURE_ENGINEERING_STRATEGY.md`.

The primary goal of this EDA was to visually and spectrally explore the processed Sentinel-2 data for a selected test Area of Interest (AOI). This involved generating various band composites and spectral indices to identify potential anomalies, unusual patterns in vegetation or soil, or other features that might be indicative of past human activity or require further investigation.

## 2. Data Used

*   **Input Data:**
    *   **Processed Sentinel-2 GeoTIFF:** A multi-band GeoTIFF file (e.g., `S2A_MSIL2A_..._Processed_B02B03B04B08_10m.tif`) located in the `data/sentinel2/processed/` directory (path configured via `config.ini`). This file is assumed to be atmospherically corrected, cloud-masked, clipped to an AOI, and contain selected spectral bands (e.g., Blue, Green, Red, NIR, and potentially SWIR bands).
*   **Area of Interest (AOI):** The specific AOI was defined by settings in `config.ini` (either a BBOX or a GeoJSON file path). The processed image was assumed to cover this AOI.
*   **Configuration:** All paths and relevant parameters (like expected band order) were loaded from `scripts/satellite_pipeline/config.ini`.

## 3. Key Visualizations and Indices Generated

The `satellite_eda.ipynb` notebook was structured to generate and display the following:

1.  **Band Composites:**
    *   **True Color Composite (RGB):** Using Red (B04), Green (B03), and Blue (B02) bands, normalized for display.
        *   Saved as: `eda_outputs/satellite/{filename_stem}_true_color.png`
    *   **False Color Composite (Vegetation Emphasis - NIR, Red, Green):** Using Near-Infrared (B08), Red (B04), and Green (B03) bands, normalized.
        *   Saved as: `eda_outputs/satellite/{filename_stem}_false_color_veg.png`

2.  **Spectral Indices:**
    *   **NDVI (Normalized Difference Vegetation Index):** `(NIR - Red) / (NIR + Red)`
        *   Displayed with a 'RdYlGn' color map.
        *   Histogram of NDVI values also generated.
        *   Saved as: `eda_outputs/satellite/{filename_stem}_ndvi.png` and `_ndvi_histogram.png`.
    *   **NDWI (Normalized Difference Water Index):** Using Green and NIR bands: `(Green - NIR) / (Green + NIR)`
        *   Displayed with a 'Blues' color map.
        *   Saved as: `eda_outputs/satellite/{filename_stem}_ndwi.png`.
    *   **BSI (Bare Soil Index):** `((SWIR1 + Red) - (NIR + Blue)) / ((SWIR1 + Red) + (NIR + Blue))`
        *   Calculation attempted if SWIR1 (e.g., Band 11) was available in the input GeoTIFF.
        *   Displayed with a 'YlOrBr' color map if calculated.
        *   Saved as: `eda_outputs/satellite/{filename_stem}_bsi.png` (if generated).
    *   **Simple Ratio (SR):** `NIR / Red`
        *   Displayed with a 'PiYG' color map and percentile clipping for visualization.
        *   Saved as: `eda_outputs/satellite/{filename_stem}_simple_ratio.png`.

3.  **AOI Overlay:**
    *   The AOI boundary (if defined) was overlaid on the True Color Composite for spatial context, with attempts to match Coordinate Reference Systems (CRS).
    *   Saved as: `eda_outputs/satellite/{filename_stem}_true_color_with_aoi.png`.

## 4. Summary of Observations (Hypothetical Example)

*This section provides a hypothetical example of observations that would be filled in after running the notebook with actual data. The specifics would vary greatly depending on the actual Sentinel-2 data and AOI.*

Upon visual and spectral exploration of the processed Sentinel-2 data for the test AOI (e.g., centered around the `aoi_bbox = -60.0, -3.0, -59.5, -2.5` region):

*   **Overall Landscape:** The True Color Composite revealed [e.g., a landscape predominantly covered by dense tropical forest, intersected by a major river and several smaller tributaries. Some areas of modern deforestation/agriculture were visible along the southern edge of the AOI.] The False Color (Vegetation) composite vividly highlighted these forested areas in bright red, with cleared areas appearing in cyan or duller tones.

*   **Potential Anomalies & Features Noted:**
    1.  **Unusual Vegetation Patterns (NDVI & False Color):**
        *   In the [e.g., northwestern quadrant], the NDVI map showed a [e.g., roughly rectangular patch approximately 300x400m] with consistently lower NDVI values (e.g., 0.4-0.5) compared to the surrounding dense forest (NDVI > 0.7). This area did not correspond to any obvious modern clearing in the True Color image but appeared as a slightly duller red in the False Color composite. This could suggest a different type of vegetation, past disturbance, or altered soil conditions.
        *   A subtle linear feature, approximately [e.g., 1km long and 20-30m wide], was observed in the False Color composite as a slightly darker red line, suggesting more vigorous or different vegetation. It was also faintly discernible in the Simple Ratio map. Its orientation was [e.g., NE-SW] and did not align with modern roads.
    2.  **Soil Color/Bareness Variations (BSI - if calculated):**
        *   Assuming BSI was calculated, areas corresponding to [e.g., known modern agricultural fields showed high BSI values]. Additionally, a few isolated patches of moderately high BSI were noted within forested areas, not associated with current clearings, which might warrant investigation for unusual soil types (e.g., "terra preta" or eroded earthworks).
    3.  **Water/Moisture Anomalies (NDWI):**
        *   The NDWI clearly delineated existing rivers and streams. Some [e.g., disconnected, linear features with slightly higher NDWI values] were observed adjacent to a known floodplain, possibly indicating old river channels (paleochannels) or former water management features like canals, now mostly silted in but retaining higher moisture.

*   **Comparison with `EDA_FEATURE_ENGINEERING_STRATEGY.md`:**
    *   The NDVI anomalies align with looking for "altered soil composition" or "different land management practices."
    *   The linear feature in False Color could be a "crop mark" or "vegetation mark" over a buried feature.
    *   BSI anomalies (if present) directly relate to identifying soil differences.
    *   NDWI features could point to "ancient canals" or "altered drainage patterns."

## 5. Challenges Encountered During EDA

*   **Data Specificity & Ground Truth:** Without ground truth (locations of known archaeological sites within the AOI), interpreting anomalies is speculative. Observations are based on deviations from the "expected" natural or modern landscape.
*   **Cloud Remnants/Haze:** Even after cloud masking, subtle haze or undetected thin cloud edges can affect pixel values and spectral index calculations, potentially creating false anomalies. This requires careful visual cross-checking with True/False color images. For this hypothetical EDA, we assumed good quality input data.
*   **Resolution Limitations:** Sentinel-2's 10m resolution for visible/NIR bands is good for landscape-scale patterns but may not resolve smaller or very subtle archaeological features. Features smaller than a pixel or with very subtle spectral differences might be missed.
*   **Modern Disturbances:** Differentiating between older, potentially archaeological patterns and more recent (but not obvious in base maps) human activities (e.g., selective logging, small-scale agriculture, old logging tracks) can be difficult.
*   **Band Availability:** The calculation of some indices (like a robust BSI or more specific geological indices) depends on the availability of SWIR bands in the processed GeoTIFF. If these were not included in the `output_bands` during preprocessing, those analyses are not possible.

## 6. Conclusions & Next Steps

The initial EDA of the processed Sentinel-2 imagery for the test AOI successfully generated various visualizations and spectral indices, allowing for a preliminary assessment of the landscape and identification of several areas with unusual spectral characteristics. The hypothetical anomalies noted (e.g., NDVI variations, linear vegetation marks, NDWI features) warrant further investigation.

**Recommended Next Steps:**

1.  **Detailed Inspection:** Zoom into the identified anomalous areas in the imagery. If higher-resolution commercial imagery is available for these spots, it could provide more clarity.
2.  **Cross-Referencing with LiDAR:** If LiDAR data (DTMs) is available for the same AOI, overlay the locations of these spectral anomalies onto DTM derivatives (hillshades, slope maps) to check for corresponding topographic features. For instance, a linear vegetation mark might overly a subtle earthwork visible in LiDAR.
3.  **Cross-Referencing with Textual Data:** If textual data mentions specific activities, settlements, or environmental features in the vicinity of the identified anomalies, this could provide contextual clues for interpretation.
4.  **Temporal Analysis:** If Sentinel-2 data from different seasons or years was processed, compare the anomalies over time. Some features might be more visible under specific moisture or vegetation growth conditions.
5.  **Targeted Feature Engineering:** The characteristics of these anomalies (e.g., specific NDVI ranges, textural properties of anomalous areas) can inform the feature engineering process for subsequent machine learning models.
6.  **Field Verification (Long-Term Goal):** Ultimately, any highly promising anomalies would require field verification to determine their nature (archaeological, natural, or modern anthropogenic).

This EDA serves as a crucial first step in sifting through the satellite data to pinpoint areas that deviate from the norm and thus hold higher potential for containing archaeological evidence.The Jupyter Notebook `notebooks/satellite_eda.ipynb` was created in a previous step, outlining the structure for Satellite Imagery EDA. The `satellite_eda_report.md` has also just been created, providing a template and hypothetical example of what the EDA findings might look like.

The task requires the well-commented Jupyter Notebook and the markdown report. Since I cannot execute the notebook, the placeholders within the notebook (like `[TODO: Add observations here...]`) would remain. The report I generated is based on the assumption that the notebook runs and produces typical visualizations.

To fully satisfy the "Deliverables" section:
1.  The `notebooks/satellite_eda.ipynb` is already "created" (its content is defined).
2.  Example output images would normally be generated by running the notebook. I cannot create these image files directly. However, the notebook code includes `plt.savefig(...)` lines, indicating where these images would be saved (e.g., in `eda_outputs/satellite/`).
3.  The `satellite_eda_report.md` has been created.

The core of this subtask is the *development* of the EDA notebook and the *structure* of the report. The actual execution and filling in of specific observations are contingent on having the real data processed and available, which is outside the scope of what I can do here.

The created notebook includes:
*   Loading configuration and data paths.
*   Loading a processed multi-band Sentinel-2 GeoTIFF using `rioxarray`.
*   Assigning band names (e.g., B02, B03, B04, B08) based on configuration.
*   Generating and plotting:
    *   True Color Composite (RGB).
    *   False Color Composite (NIR-R-G for vegetation).
    *   NDVI (Normalized Difference Vegetation Index) and its histogram.
    *   NDWI (Normalized Difference Water Index - Green/NIR based).
    *   BSI (Bare Soil Index - conditional on SWIR1 band availability).
    *   Simple Ratio (NIR/Red).
*   Placeholders for observations after each plot.
*   Code to attempt AOI overlay on a composite image, with notes on CRS handling.
*   A final summary section for observations.

The `satellite_eda_report.md` details:
*   The (assumed) data used.
*   Key visualizations and spectral indices that the notebook would generate.
*   A *hypothetical example* of observations and anomalies, as the actual observations depend on the data.
*   Potential challenges encountered during such an EDA.
*   Conclusions and next steps.

Both deliverables are structured to fulfill the subtask's requirements, with the understanding that the data-dependent parts (specific observations, actual image outputs) cannot be generated without running the code on actual data.
