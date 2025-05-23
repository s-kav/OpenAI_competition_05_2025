# Procedures for Verifying Potential Interest Zones (PIZs)

## 1. Introduction

This document outlines the standardized procedures for verifying high-scoring Potential Interest Zones (PIZs) identified by the scoring system detailed in `notebooks/piz_identification_scoring.ipynb`. The goal of this verification process is to systematically assess the archaeological potential of these top N PIZs using at least two independent methods, thereby increasing confidence in their nature before any potential resource-intensive investigations.

The verification methods described herein are based on the strategies outlined in the `SITE_PREDICTION_VERIFICATION_STRATEGY.md` document. This document aims to provide a practical, step-by-step guide for applying these verification methods.

## 2. Selection of Top PIZs for Verification

The PIZs to be subjected to these verification procedures will be selected based on their ranking from the heuristic scoring system implemented in `piz_identification_scoring.ipynb`.

*   **Selection Criteria:** The top N PIZs (e.g., top 5, 10, or a number determined by available resources/time) with the highest overall scores will be prioritized for verification.
*   **Review of Scores:** Before final selection, the contributing factors to the high scores will be briefly reviewed to ensure a diverse range of evidence types or particularly strong single-source evidence is being considered, if desired. For example, one might prioritize a PIZ with a slightly lower score but evidence from three data types over a PIZ with a slightly higher score based only on very strong LiDAR evidence.

## 3. Detailed Procedures for Primary Verification Methods

We will employ at least two distinct primary verification methods for each selected PIZ. The following are two chosen methods with their detailed procedures:

### 3.1. Method 1: Cross-Data Corroboration & Detailed Multi-Source Re-Analysis

This method combines elements of "Cross-Data Corroboration" and "Detailed Multi-Source Re-Analysis" from the strategy document. It focuses on a deep dive into existing and potentially new, targeted data for the specific PIZ.

*   **Objective:** To find converging evidence for the PIZ's features across different datasets and through more focused re-analysis of existing data.

*   **Data Needed:**
    1.  **PIZ Definition:** Coordinates/polygon of the PIZ from `piz_ranked_list.geojson`.
    2.  **Original Anomaly Data:** The specific LiDAR, Satellite, and/or Textual features that defined the PIZ.
    3.  **Full Resolution Processed Data:** Access to the full-resolution processed DTMs, hillshades, spectral index rasters, and band composites covering the PIZ.
    4.  **Raw Data (Optional but Recommended):** Access to the original raw LiDAR point clouds (LAS/LAZ) and Sentinel-2 SAFE files for the PIZ area, if deeper re-processing is warranted.
    5.  **High-Resolution Satellite Imagery (If Available/Acquirable):** If the project has access to higher-resolution satellite imagery (e.g., PlanetScope, commercial archives like Maxar) for the PIZ coordinates, this would be invaluable.
    6.  **Historical Maps:** Georeferenced historical maps covering the PIZ area (from sources identified in Phase 1).
    7.  **Relevant Textual Corpus:** The cleaned text files, especially those whose geocoded entities contributed to the PIZ.

*   **Tools/Software to be Used:**
    1.  **GIS Software:** QGIS, ArcGIS, or similar for detailed visual inspection, overlay analysis, and map creation.
    2.  **Remote Sensing Software (Optional):** SNAP, ENVI, or Python libraries (`rasterio`, `xarray`, `spyndex`) for re-analyzing satellite data (e.g., generating alternative indices, applying different stretches, texture analysis).
    3.  **LiDAR Software (Optional):** CloudCompare, PDAL, LAStools (if re-processing raw LiDAR) for generating new DTM derivatives (e.g., different hillshade parameters, higher-resolution DTM for a small area, alternative visualizations like Sky-View Factor if tools are available).
    4.  **Text Analysis Tools:** Python scripts for searching keywords in context within the textual corpus, referencing outputs from `textual_eda_openai.ipynb`.

*   **Step-by-Step Analytical Process:**
    1.  **Define Micro-AOI:** Create a slightly larger bounding box around the specific PIZ to provide immediate context.
    2.  **LiDAR Re-evaluation:**
        *   Load the PIZ polygon into GIS software. Overlay it on the existing DTM and various hillshade derivatives (from different azimuths, SVF if available).
        *   Minutely examine the topographic features within the PIZ. Are their shapes, sizes, and arrangements clearly artificial or could they be natural?
        *   If raw LiDAR is available and features are ambiguous, consider re-processing the point cloud for this micro-AOI with different classification parameters or generating a higher-resolution DTM if point density allows.
        *   Generate new, targeted visualizations (e.g., specific hillshade angles not previously computed, slope, aspect, LRM) focused on the PIZ.
    3.  **Satellite Imagery Re-evaluation:**
        *   Overlay the PIZ polygon on all available processed satellite bands, true/false color composites, and spectral indices (NDVI, NDWI, BSI, etc.).
        *   Look for subtle spectral signatures, vegetation patterns, or soil marks that spatially correlate with the features identified in LiDAR or textual data.
        *   If high-resolution imagery is available, meticulously inspect it for visible structures, earthworks, or patterns that might have been too small for Sentinel-2.
        *   Consider applying different image enhancement techniques (stretches, filters) or calculating alternative/custom spectral indices specifically for the PIZ area to highlight subtle features.
        *   If time-series Sentinel-2 data is available (multiple dates processed), examine the PIZ across different dates/seasons for changes or features that appear under specific conditions.
    4.  **Textual Data Re-evaluation:**
        *   If the PIZ was influenced by textual mentions, re-read the source texts, focusing on descriptions related to the PIZ's specific location and the types of features observed in LiDAR/Satellite data.
        *   Perform keyword searches in the broader textual corpus for terms matching the observed feature morphologies or the PIZ's general location.
        *   Use the OpenAI-generated NER outputs to see if any `ARCHAEOLOGICAL_SITE`, `SETTLEMENT_STRUCTURE`, or relevant `PLACE_NAME` entities spatially correlate closely with the PIZ.
    5.  **Historical Map Overlay:**
        *   Overlay georeferenced historical maps onto the PIZ in GIS.
        *   Look for any notations, symbols (e.g., for villages, ruins, paths, missions, rapids, old land use), or drawn features on the historical maps that coincide with or are very near the PIZ. Note map scale and estimated accuracy.
    6.  **Synthesize Findings:** Combine all observations. Does the evidence from different sources converge and support an anthropogenic origin for the features within the PIZ?

*   **Criteria for Successful Verification (Confidence Boost):**
    *   **Strong Positive:** Clear, unambiguous evidence of anthropogenic features from at least two different data types that spatially correlate within the PIZ (e.g., a geometric earthwork in LiDAR matches a distinct geometric vegetation pattern in high-res satellite imagery, and a historical map notes a "fort" in the vicinity).
    *   **Moderate Positive:** Suggestive evidence from multiple sources, or very clear evidence from one primary source (e.g., very distinct LiDAR earthworks) with some plausible, though not definitive, supporting hints from another source.
    *   **Inconclusive:** Features are ambiguous, could be natural, or evidence from different sources is weak or conflicting.
    *   **Likely Non-Archaeological:** Clear evidence suggests features are natural (e.g., geological formations, fluvial processes) or modern anthropogenic (e.g., recent logging tracks, modern agricultural patterns not previously filtered).

### 3.2. Method 2: Comparative Analysis with Known Archaeological Sites (Literature-Based)

This method focuses on comparing the characteristics of features within the PIZ to documented archaeological sites in the Amazon or similar tropical environments.

*   **Objective:** To determine if the morphology, scale, arrangement, and environmental setting of features within the PIZ are consistent with known types of Amazonian archaeological sites.

*   **Data Needed:**
    1.  **PIZ Characterization:** Detailed description of the features within the PIZ (from Method 1 analysis):
        *   Type (e.g., mound, linear earthwork, enclosure, depression, vegetation mark).
        *   Dimensions (length, width, height/depth, area).
        *   Shape (circular, rectangular, linear, irregular).
        *   Arrangement (isolated, clustered, patterned).
        *   Topographic setting (e.g., hilltop, floodplain, interfluve, slope).
        *   Relationship to water sources.
    2.  **Archaeological Literature Database:** Access to academic papers, books, excavation reports, and databases describing known Amazonian archaeological sites. This includes typologies, site plans, photographs, and environmental context. (Sources identified in Phase 1, e.g., JSTOR, Academia.edu, university repositories, specific Amazonian archaeology journals).
    3.  **Image/Map Database of Known Sites:** Collections of published maps, DTM visualizations, or satellite images of verified archaeological sites in the Amazon.

*   **Analytical Process:**
    1.  **Characterize PIZ Features:** Based on the detailed re-analysis (Method 1), create a profile for the primary features within the PIZ (e.g., "PIZ contains three circular mounds, approx. 15-20m diameter, 1-1.5m high, located on a bluff overlooking a small stream").
    2.  **Literature Search Strategy:**
        *   Identify keywords based on the PIZ feature characteristics and its general geographic region (if known, e.g., "Upper Xingu ring villages," "Amazonian causeways," "várzea mounds," "interfluvial geoglyphs").
        *   Search academic databases and literature for descriptions and examples of sites matching these keywords or characteristics.
    3.  **Comparative Evaluation:**
        *   For each documented site type found in the literature that appears relevant, compare its characteristics (morphology, dimensions, construction techniques if known, layout, environmental setting) with those of the PIZ features.
        *   Note strong similarities (e.g., "The mounds in PIZ #X are morphologically very similar in size and shape to documented 'tesos' from Marajó Island").
        *   Note significant differences (e.g., "While the PIZ contains linear features, they are much smaller and less regularly patterned than known pre-Columbian raised field systems in the region").
        *   Consider the known chronological periods and cultural affiliations of the comparative sites.
    4.  **Assess Fit:** Determine how well the PIZ features fit within the known range of Amazonian archaeological manifestations.

*   **Criteria for Successful Verification (Confidence Boost):**
    *   **Strong Positive:** The features within the PIZ show a strong and consistent match in multiple aspects (morphology, size, layout, environmental setting) to a well-documented type of Amazonian archaeological site.
    *   **Moderate Positive:** The PIZ features share some key characteristics with known site types but also exhibit some differences or are less clear-cut. The analogy provides a plausible, but not definitive, interpretation.
    *   **Weak/No Match:** The PIZ features do not clearly correspond to any known types of archaeological sites in the region, or they more closely resemble natural landforms or known modern disturbances.
    *   **Potentially New Type (Rare):** If features are clearly artificial but do not match known types, this could (very cautiously) suggest a new or undocumented form of site, requiring even more rigorous future investigation.

## 4. Procedures for Secondary/Alternative Verification Methods (Briefly)

If the primary methods are inconclusive or to provide further supporting evidence, the following can be considered (referencing `SITE_PREDICTION_VERIFICATION_STRATEGY.md`):

*   **Consulting External Databases/Experts:**
    *   **Data/Approach:** Check publicly accessible, non-competition archaeological databases for the region (if any exist and are permitted). If allowed by competition rules, consult (without revealing exact PIZ locations if sensitive) with archaeologists specializing in the Amazon about the *types* of features observed.
    *   **Usefulness:** Can quickly confirm if a PIZ corresponds to an already inventoried (but perhaps obscurely published) site. Expert opinion can offer interpretative insights on feature types.
*   **Environmental/Simulation Modeling:**
    *   **Data/Approach:** Use DTMs from the PIZ to model local hydrology (for potential canals, water management), visibility/intervisibility (for defensive/ceremonial sites), or resource accessibility (suitability for agriculture, proximity to raw materials based on geological/soil maps if available).
    *   **Usefulness:** Assesses if the PIZ's environmental context is congruent with a hypothesized function.
*   **Advanced Remote Sensing Analysis (if not already exhausted):**
    *   **Data/Approach:** Apply more specialized remote sensing techniques to the PIZ area, such as advanced texture analysis, object-based image analysis (OBIA) for feature segmentation, or different LiDAR visualization techniques (e.g., openness, sky-view factor if not done in primary EDA).
    *   **Usefulness:** May reveal more subtle aspects of features or help delineate their extent more precisely.

## 5. Documentation of Verification Results

Systematic documentation is crucial for each PIZ undergoing verification. A structured report or a dedicated section in a project database/spreadsheet should be maintained.

*   **Information to Record for Each PIZ:**
    1.  **PIZ ID:** Unique identifier.
    2.  **Original Score & Rank:** From the `piz_identification_scoring.ipynb` output.
    3.  **Date of Verification:**
    4.  **Verifier(s) Name(s):**
    5.  **Verification Methods Applied:** List all methods used for this PIZ.
    6.  **For each method applied:**
        *   **Data Sources Used:** Specific files, map titles, literature citations.
        *   **Tools Used:** Software versions, specific algorithms/parameters if applicable.
        *   **Detailed Findings:** Objective description of observations (e.g., "Historical map X from 1780 shows a 'mission' symbol within 200m of the PIZ centroid." "Comparative analysis reveals mound dimensions are consistent with Type Y sites described by Author Z (2005).").
        *   **Images/Screenshots:** Key visual evidence supporting the findings (e.g., zoomed-in views of anomalies, map overlays, comparative images from literature). Store these in an organized manner, linked to the PIZ ID.
        *   **Outcome/Confidence Level for this Method:** (e.g., Strong Positive, Moderate Positive, Inconclusive, Likely Non-Archaeological).
    7.  **Overall Verification Summary:**
        *   A synthesis of findings from all applied verification methods.
        *   An overall confidence assessment (e.g., High, Medium, Low) that the PIZ represents a genuine archaeological site or area of high archaeological potential.
        *   Justification for this assessment.
    8.  **Revised PIZ Score/Priority (Optional):** The verification findings might lead to a qualitative or even quantitative adjustment of the PIZ's priority.
    9.  **Recommendations for Future Action:** (e.g., "Recommend for Phase 5 (fieldwork simulation/planning)," "Requires further specific remote sensing analysis," "Downgrade - likely natural feature").

This structured documentation will ensure transparency, traceability, and provide a solid basis for any subsequent phases of the project, including potential fieldwork planning or final reporting.The document `PIZ_VERIFICATION_PROCEDURES.md` has been created.

It includes the following sections as requested:

1.  **Introduction:** States the goal of verifying top N PIZs using at least two independent methods and references `SITE_PREDICTION_VERIFICATION_STRATEGY.md`.
2.  **Selection of Top PIZs:** Explains selection based on highest scores from `piz_identification_scoring.ipynb` and potential review of scoring factors.
3.  **Detailed Procedures for at Least Two Primary Verification Methods:**
    *   **Method 1: Cross-Data Corroboration & Detailed Multi-Source Re-Analysis:**
        *   Details the objective, data needed (PIZ definition, original anomaly data, full/raw resolution data, potential high-res satellite imagery, historical maps, textual corpus).
        *   Lists tools/software (GIS, Remote Sensing software, LiDAR software, text analysis tools).
        *   Provides a step-by-step analytical process (Define Micro-AOI, LiDAR Re-evaluation, Satellite Imagery Re-evaluation, Textual Data Re-evaluation, Historical Map Overlay, Synthesize Findings).
        *   Outlines criteria for successful verification (Strong Positive, Moderate Positive, Inconclusive, Likely Non-Archaeological).
    *   **Method 2: Comparative Analysis with Known Archaeological Sites (Literature-Based):**
        *   Details the objective, data needed (PIZ characterization, archaeological literature database, image/map database of known sites).
        *   Provides an analytical process (Characterize PIZ Features, Literature Search Strategy, Comparative Evaluation, Assess Fit).
        *   Outlines criteria for successful verification (Strong Positive, Moderate Positive, Weak/No Match, Potentially New Type).
4.  **Procedures for Secondary/Alternative Verification Methods (Briefly):**
    *   Lists and briefly describes "Consulting External Databases/Experts," "Environmental/Simulation Modeling," and "Advanced Remote Sensing Analysis."
5.  **Documentation of Verification Results:**
    *   Specifies how results will be documented (structured report or database section).
    *   Lists information to be recorded for each PIZ (ID, score, date, verifier, methods, data, tools, findings, images, outcome/confidence level, overall summary, revised score, recommendations).

The document provides a practical and systematic guide for the verification phase, ensuring clarity and actionable procedures based on previously discussed tools and data types.
