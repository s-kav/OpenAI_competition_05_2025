# EDA and Feature Engineering Strategy for Amazonian Archaeology

This document outlines the Exploratory Data Analysis (EDA) strategy and potential features to be engineered from Satellite Imagery, LiDAR, and Textual Data. The goal is to identify indicators relevant to discovering Amazonian archaeological sites.

## 1. Satellite Imagery (Processed Sentinel-2 Data)

### 1.1. EDA Goals & Questions

*   **Main Questions:**
    *   Are there distinct spectral signatures or vegetation patterns associated with known archaeological sites compared to surrounding areas?
    *   Can we identify unusual clearings, geometric shapes, or linear features in vegetation or soil that are not explainable by modern activity?
    *   How does land cover (forest, savanna, agriculture, water bodies) vary across the AOI, and are there correlations with potential site locations?
    *   What is the extent of modern human impact (deforestation, agriculture, urban areas) that might obscure or mimic archaeological sites?
    *   If time-series data is available, what historical changes in land use or vegetation patterns can be observed that might point to past human modifications?
*   **Specific Characteristics to Explore:**
    *   **Pixel Value Distributions:** For each band and derived index, understand their statistical distributions (histograms, mean, median, variance).
    *   **Band Correlations:** How do different spectral bands correlate with each other?
    *   **Spectral Profiles:** Analyze the spectral signatures of known archaeological sites (if available as ground truth) versus non-site areas.
    *   **Spatial Patterns:** Visual inspection for anomalies, supported by quantitative measures of texture and shape.
    *   **Seasonal Variations:** If data from different seasons is available, how do spectral signatures change?
    *   **Cloud Cover Impact:** Assess the quality of data and the impact of cloud/shadow masking on usability.

### 1.2. Potential Archaeological Indicators (Features to Engineer)

*   **Spectral Indices:**
    *   **NDVI (Normalized Difference Vegetation Index):** `(NIR - Red) / (NIR + Red)`
        *   *Relevance:* Indicates vegetation health and density. Anomalous NDVI values (e.g., stressed or overly vigorous vegetation in specific patterns) can indicate buried structures, altered soil composition due to past human activity (e.g., "terra preta" - Amazonian Dark Earths), or different land management practices.
    *   **NDWI (Normalized Difference Water Index):** `(Green - NIR) / (Green + NIR)` or `(NIR - SWIR) / (NIR + SWIR)` (using SWIR1 like Sentinel-2 Band 11)
        *   *Relevance:* Highlights open water bodies and soil moisture. Can help identify ancient canals, moats, reservoirs, or areas with altered drainage patterns due to human earthworks.
    *   **SAVI/MSAVI (Soil Adjusted Vegetation Index / Modified SAVI):** Variants of NDVI that account for soil brightness.
        *   *Relevance:* Useful in areas with partial vegetation cover, where soil influence on NDVI is strong. Can help differentiate subtle vegetation changes from soil background variations. Example MSAVI2: `(1/2) * (2 * (NIR + 1) - sqrt((2 * NIR + 1)^2 - 8 * (NIR - Red)))`
    *   **EVI (Enhanced Vegetation Index):** Similar to NDVI but corrects for atmospheric influences and canopy background. `G * ((NIR - Red) / (NIR + C1 * Red - C2 * Blue + L))` (Coefficients C1, C2, L, G vary by sensor; for Sentinel-2, specific adaptations exist).
        *   *Relevance:* More sensitive in high biomass regions, potentially highlighting subtle vegetation stress or enrichment.
    *   **NDMI (Normalized Difference Moisture Index):** `(NIR - SWIR1) / (NIR + SWIR1)` (using Sentinel-2 Band 8A and Band 11)
        *   *Relevance:* Sensitive to vegetation water content. Could indicate areas with different moisture retention due to past soil management or earthworks.
    *   **Clay Minerals Ratio:** `SWIR1 / SWIR2` (e.g., Sentinel-2 Band 11 / Band 12)
        *   *Relevance:* Can highlight areas with exposed soils rich in clay, potentially indicative of pottery manufacturing sites or specific types of earthworks.
    *   **Iron Oxide Ratio:** `Red / Blue` (e.g., Sentinel-2 Band 4 / Band 2)
        *   *Relevance:* Can indicate areas with soils rich in iron oxides, sometimes associated with specific human activities or types of earth.
    *   **Principal Component Analysis (PCA) on Bands:** Not an index, but PCA can transform correlated bands into uncorrelated principal components. Some components might highlight subtle spectral variations related to archaeology that are not obvious in standard bands/indices.

*   **Textural Features & Patterns:** (Often computed on single bands or PCA components)
    *   **Edge Detection Filters:** (e.g., Sobel, Canny, Laplacian filters) to highlight linear features, outlines of geometric shapes.
    *   **GLCM (Gray-Level Co-occurrence Matrix) Textures:**
        *   *Metrics:* Homogeneity, Contrast, Dissimilarity, Energy, Correlation, ASM (Angular Second Moment).
        *   *Relevance:* Quantify the spatial relationship of pixel values. Anomalous textural patterns (e.g., unusually smooth or rough areas, repetitive patterns) can indicate agricultural fields, settlement layouts, or large earthworks.
    *   **Fourier Transform:** To identify periodic patterns or directional features in the imagery.
    *   **Shape Descriptors:** For features identified through segmentation (e.g., compactness, eccentricity, orientation) to quantify if shapes are anthropogenic.
    *   **Lineament Density/Orientation:** Analysis of detected linear features. Consistent orientations or high densities can be indicative of causeways, canals, or field boundaries.

*   **Temporal Changes (Time-Series Analysis):**
    *   **Change Detection:** Comparing images from different time periods (e.g., NDVI differencing, image differencing after radiometric normalization).
        *   *Relevance:* Can reveal features that are only visible under specific moisture or vegetation conditions, or show how landscapes have changed, potentially revealing older, now obscured features. Sudden appearances or disappearances of vegetation patterns.
    *   **Phenological Metrics:** Analyzing vegetation green-up, peak, and senescence timing. Differences might indicate altered soil or drainage.
    *   **Historical Land Use Reconstruction:** Identify areas of past deforestation or agriculture that have since regrown, which might be targets for archaeological investigation.

## 2. LiDAR Data (DTMs, Hillshades)

### 2.1. EDA Goals & Questions

*   **Main Questions:**
    *   Can we detect subtle, low-relief earthworks (mounds, platforms, causeways, canals, defensive structures, agricultural features like raised fields or terraces) that are obscured by dense vegetation in imagery or on the ground?
    *   What are the typical morphological characteristics (size, shape, height/depth, orientation, spacing) of known or suspected archaeological features in the DTM?
    *   Are there patterns in the distribution or orientation of these topographic features?
    *   How do different DTM visualization techniques enhance the visibility of these features?
    *   Can we differentiate between natural landforms and anthropogenic earthworks based on their topographic signature?
*   **Specific Characteristics to Explore:**
    *   **Elevation Histograms:** To understand the general topography and identify anomalous elevation ranges.
    *   **Slope and Aspect Distributions:** Analyze overall terrain ruggedness and preferred orientations. Anomalies might indicate artificial terracing or embankments.
    *   **Surface Roughness:** Quantify variations in local relief.
    *   **Profile Analysis:** Create cross-sectional profiles across suspected features to analyze their shape and dimensions.
    *   **Drainage Patterns:** Derived from DTMs, can show how water flow might have been altered by human constructions.

### 2.2. Potential Archaeological Indicators (Features to Engineer)

*   **Subtle Topographic Features:**
    *   **Micro-relief Analysis:** Exaggerating very small elevation differences.
    *   **Detection of Geometric Shapes:** Identifying rectangular, circular, or linear patterns in elevation data.
    *   **Mound/Depression Detection:** Algorithms that search for localized positive or negative relief features.
    *   **Linear Feature Extraction:** Identifying ridges (e.g., causeways, embankments) or depressions (e.g., canals, ditches).
    *   **Slope Break Analysis:** Identifying sharp changes in slope that might delineate edges of platforms or terraces.
    *   **Pattern Recognition:** Identifying repeating patterns like raised fields or settlement layouts.

*   **Visualization Techniques for Feature Identification (and as input to further analysis):**
    *   **Hillshade (Multi-directional & Single):** Essential for visual interpretation. Features can be engineered from hillshade images themselves (e.g., textural analysis on hillshades).
        *   *Averaged multi-directional hillshades* provide even illumination.
        *   *PCA on multiple hillshades* from different azimuths can enhance subtle features.
    *   **Slope Maps:** Clearly show changes in gradient, highlighting edges of features.
    *   **Aspect Maps:** Show the orientation of slopes. Consistent aspects over an area can indicate terracing.
    *   **Sky-View Factor (SVF) / Openness:** Measures the portion of the sky visible from each point. Excellent for highlighting subtle depressions (low SVF) or raised features (high positive openness).
    *   **Local Relief Models (LRM):** Removing regional elevation trends to emphasize local variations.
    *   **DEM Differencing (if multi-temporal LiDAR exists):** To show changes in topography over time (rare for archaeology but possible in dynamic landscapes).
    *   **Combined Visualizations:** E.g., transparent hillshade overlaid on a color-ramped DTM or slope map.

## 3. Textual Data (Cleaned Texts)

### 3.1. EDA Goals & Questions

*   **Main Questions:**
    *   What geographic locations (place names, rivers, mountains) are mentioned frequently, and can they be mapped?
    *   What Indigenous groups, settlements, or polities are described?
    *   Are there descriptions of ancient structures, earthworks, agricultural practices, or resource use?
    *   What are the characteristics of described settlements (size, materials, defensive features, proximity to resources)?
    *   What trade routes, travel paths, or interactions between groups are mentioned?
    *   Are there temporal references that can help date descriptions or events?
    *   What is the general sentiment or focus of different types of documents (e.g., colonial reports vs. ethnographic studies vs. archaeological papers)?
*   **Specific Characteristics to Explore:**
    *   **Frequency Distributions:** Of words, n-grams, named entities.
    *   **Keyword Search & Concordance:** Examine the context of specific archaeological terms (e.g., "earthwork," "mound," "village," "causeway," "terra preta").
    *   **Document Lengths & Language Distribution:** Basic corpus statistics.
    *   **Co-occurrence Networks:** Which terms or entities frequently appear together?

### 3.2. Potential Archaeological Indicators (Features to Engineer)

*   **Extracted Entities:**
    *   **Geographic Place Names (Toponyms):** Rivers, mountains, regions, specific settlement names.
    *   **Ethnonyms/Group Names:** Names of Indigenous tribes, communities, or historically mentioned groups.
    *   **Archaeological Feature Descriptions:** Mentions of "mounds," "earthworks," "palisades," "villages," "fields," "ruins," "artifacts," "ceramics," "stone tools."
    *   **Resource Mentions:** Gold, salt, clay, specific plants (e.g., manioc, maize), animals.
    *   **Temporal Expressions:** Dates, relative time references ("many years ago," "ancient times").
    *   **Travel/Route Descriptions:** "Upriver," "two days journey," "path leading to X."
    *   **Cultural Practices:** Descriptions of agriculture, hunting, warfare, rituals that might leave archaeological traces.
*   **Co-occurrence of Terms/Concepts:**
    *   *Feature:* Frequency of co-occurrence of a specific place name with terms like "settlement," "ruins," or "earthworks."
    *   *Feature:* Co-occurrence of resource mentions with specific group names or locations.
*   **Sentiment/Descriptive Language:**
    *   *Feature:* Sentiment scores (positive, negative, neutral) associated with descriptions of locations or groups (requires careful interpretation due to colonial bias).
    *   *Feature:* Presence of descriptive adjectives related to size ("large," "small"), material ("earthen," "stone"), or condition ("abandoned," "fortified") when describing potential sites.

## 4. Role of OpenAI Models in EDA/Feature Engineering (Textual Data)

OpenAI models can significantly accelerate and enhance EDA and feature engineering for textual data:

*   **Named Entity Recognition (NER):**
    *   *o3/o4 mini, GPT-4.1:* Fine-tune or use few-shot prompting to identify custom entity types relevant to Amazonian archaeology and history (e.g., `ANCIENT_SETTLEMENT_NAME`, `ETHNOGRAPHIC_GROUP`, `ARCHAEOLOGICAL_FEATURE_TYPE`, `LOCAL_RESOURCE`, `HISTORICAL_EVENT_AMAZONIA`). This is more powerful than off-the-shelf NER which might miss nuanced terms.
    *   *Example:* Extracting "várzea mounds" as an `ARCHAEOLOGICAL_FEATURE_TYPE` or "Tapajós" as an `ETHNOGRAPHIC_GROUP`.
*   **Topic Modeling:**
    *   *o3/o4 mini, GPT-4.1:* Can be prompted to identify latent themes or topics within a collection of documents (e.g., "descriptions of riverine settlements," "colonial expeditions and resource extraction," "ethnographic accounts of agricultural practices"). These topics can then become categorical features for documents or guide further analysis.
    *   *Example:* A document might be strongly associated with the topic "fortified villages along major rivers."
*   **Relationship Extraction:**
    *   *o3/o4 mini, GPT-4.1:* Extract relationships between entities.
        *   *Example:* From "The Omagua people built their villages along the Amazon river," extract: `(Omagua, LOCATED_NEAR, Amazon River)` or `(Omagua, BUILT, Villages)`.
        *   These extracted relationships can form a knowledge graph or be used as features (e.g., count of "located near river" relationships for a specific group).
*   **Geocoding/Disambiguating Place Names:**
    *   *o3/o4 mini, GPT-4.1:* Given a place name mentioned in a text and its surrounding context, prompt the model to:
        *   Suggest potential modern equivalents or geographic coordinates (if the place is known).
        *   Disambiguate between multiple places with the same name based on context.
        *   Provide a qualitative assessment of the location's likely region if precise coordinates are not possible.
    *   *Example:* Disambiguating which "Rio Negro" is being referred to based on other nearby mentioned locations or the described environment.
*   **Generating Initial Summaries:**
    *   *o3/o4 mini, GPT-4.1:* Quickly summarize long documents or collections of documents to highlight key information relevant to archaeology. This helps prioritize texts for closer manual reading and detailed feature extraction.
    *   *Example:* "Summarize this colonial diary, focusing on any mentions of large native settlements, earthworks, or agricultural systems."

## 5. Cross-Data Type Analysis Ideas (Initial Thoughts)

*   **Text-to-Remote Sensing:**
    *   Use place names or geographic descriptions extracted from texts to define specific AOIs for targeted analysis of satellite imagery or LiDAR data.
    *   If texts describe specific types of earthworks or settlement patterns, look for these morphologies in LiDAR DTMs/hillshades in the suspected regions.
    *   Correlate descriptions of vegetation or soil (e.g., "fertile black earth," "dense forest with fruit trees") with spectral indices from satellite imagery.
*   **Remote Sensing-to-Text:**
    *   If satellite imagery or LiDAR reveals an unexplainable anomaly (e.g., a large geometric earthwork), search the textual corpus for mentions of settlements, battles, or significant features in that approximate geographic region.
*   **Combined Features for Predictive Modeling:**
    *   **Proximity Features:** Distance from a point (e.g., a pixel or a potential site) to the nearest textually-mentioned ancient settlement, river, or resource.
    *   **Density Features:** Number of textually-mentioned archaeological sites or relevant keywords within a certain radius of a location identified by remote sensing.
    *   **Concordance Score:** A score indicating how well the features from remote sensing (e.g., specific spectral signature + topographic anomaly) match textual descriptions of sites in that area.
    *   **Weighted Evidence:** Combine probabilities or likelihood scores from models trained independently on each data type. For example, an area with high probability from LiDAR analysis and textual mentions of a nearby settlement would receive a higher overall score.
    *   **Environmental Context from Remote Sensing + Textual Clues:** Analyze if areas with certain environmental characteristics (e.g., specific NDVI range, proximity to water from satellite data) that are also mentioned in texts as favorable for settlement show higher concentrations of LiDAR anomalies.

This EDA and feature engineering strategy will be iterative. Initial findings will guide further refinement of questions, exploration techniques, and feature definitions.Okay, I've created the `EDA_FEATURE_ENGINEERING_STRATEGY.md` document.

It includes:

1.  **For Satellite Imagery (Sentinel-2):**
    *   EDA Goals & Questions (e.g., distinct spectral signatures, unusual clearings, land cover correlations).
    *   Potential Archaeological Indicators (Spectral Indices: NDVI, NDWI, SAVI, EVI, NDMI, Clay/Iron Oxide Ratios, PCA; Textural Features: Edge detection, GLCM, Fourier, Shape descriptors; Temporal Changes: Change detection, phenology).

2.  **For LiDAR Data (DTMs, Hillshades):**
    *   EDA Goals & Questions (e.g., detecting subtle earthworks, feature morphology, differentiating natural vs. anthropogenic).
    *   Potential Archaeological Indicators (Micro-relief, geometric shapes, mound/depression detection, linear features, slope breaks; Visualization techniques: Hillshade, Slope, Aspect, SVF, LRM).

3.  **For Textual Data (Cleaned Texts):**
    *   EDA Goals & Questions (e.g., mapping place names, identifying groups/settlements, descriptions of structures/practices, temporal references).
    *   Potential Archaeological Indicators (Extracted Entities: Toponyms, Ethnonyms, Feature Descriptions, Resources, Temporal Expressions, Routes; Co-occurrence of terms; Sentiment/Descriptive Language).

4.  **Role of OpenAI Models in EDA/Feature Engineering (Textual Data):**
    *   Expanded on using models for tailored NER, topic modeling, relationship extraction, geocoding/disambiguation, and generating summaries.

5.  **Cross-Data Type Analysis Ideas:**
    *   Text-to-Remote Sensing (e.g., textual mentions guiding targeted LiDAR/Satellite analysis).
    *   Remote Sensing-to-Text (e.g., anomalies guiding text searches).
    *   Combined Features for Predictive Modeling (e.g., proximity features, density features, concordance scores, weighted evidence).

This document should provide a solid strategic foundation for the EDA and feature engineering phase of the project.
