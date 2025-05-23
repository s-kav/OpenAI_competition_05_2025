# Phase 4: Site Prediction and Verification Model Development Strategy

This document outlines the strategy for Phase 4, focusing on integrating insights from previous Exploratory Data Analysis (EDA) phases, developing a system to predict and prioritize potential archaeological sites (Potential Interest Zones - PIZs), and defining methods for their verification.

## 1. Methodology for Integrating EDA Insights

The core of this phase is to synthesize findings from LiDAR, Satellite, and Textual EDA to identify geographically specific PIZs where the probability of discovering archaeological sites is heightened.

### 1.1. Combining Multi-Source Evidence

Findings from each data type will be transformed into spatial layers or geographically referenced attributes that can be overlaid and analyzed together.

*   **LiDAR EDA Insights:**
    *   **Input:** Locations/polygons of topographic anomalies (mounds, earthworks, linear features, geometric shapes), areas with distinct slope/aspect/SVF characteristics identified during `lidar_eda.ipynb`.
    *   **Representation:** Vector layers (polygons, lines, points) representing these features, potentially with attributes describing feature type, size, clarity, and confidence.
*   **Satellite EDA Insights:**
    *   **Input:** Areas with unusual vegetation patterns (from NDVI, False Color), distinct spectral signatures (from indices like BSI, Clay/Iron Oxide Ratios), potential clearings, or structural patterns (from texture analysis) identified during `satellite_eda.ipynb`.
    *   **Representation:** Raster anomaly maps (e.g., pixels deviating significantly from local norms for a given index) or vector polygons outlining anomalous zones. Attributes could include anomaly type, intensity, and size.
*   **Textual EDA (OpenAI-driven) Insights:**
    *   **Input:**
        *   Geocoded/disambiguated place names (toponyms, archaeological sites, Indigenous group locations) from `textual_eda_openai.ipynb`.
        *   Areas described in texts as having settlements, earthworks, specific resources, or historical events.
        *   Relationships extracted (e.g., "Group X lived near River Y," "Site Z had Feature A").
    *   **Representation:**
        *   For specific place names: Point layers with attributes like place name, confidence of geocoding, historical period mentioned.
        *   For broader areas described: Polygons representing the general vicinity, attributed with summaries of textual descriptions or keywords.
        *   For relationships: These might inform the attributes of the point/polygon features or guide the search for corroborating evidence (e.g., if Group X is associated with "mounds," prioritize mound-like LiDAR features near geocoded locations of Group X).

### 1.2. Creating Potential Interest Zones (PIZs)

PIZs will be delineated based on the spatial convergence of evidence from two or more data types. This will be achieved through Geographic Information System (GIS) overlay operations.

*   **Method:**
    1.  **Spatial Buffering & Proximity Analysis:**
        *   For point features (e.g., geocoded textual mentions), create buffer zones (e.g., 100m, 500m, 1km radius) to account for spatial uncertainty in textual descriptions or geocoding. The buffer size will depend on the perceived accuracy of the textual reference.
        *   For linear features (e.g., LiDAR-identified causeways, satellite-identified linear vegetation anomalies), create buffer zones along their lengths.
    2.  **Overlay Analysis (Intersection/Union):**
        *   **Scenario A (LiDAR + Satellite):** Intersect LiDAR anomaly polygons/buffers with satellite imagery anomaly polygons/rasters. Zones with overlap are strong PIZs.
            *   *Example:* An area with LiDAR-detected mounds that also shows a distinct circular vegetation pattern in NDVI.
        *   **Scenario B (Textual + Remote Sensing):** Intersect geocoded textual mention buffers with LiDAR and/or satellite anomaly layers.
            *   *Example:* A 500m buffer around a textually mentioned "ancient village" that overlaps with identified LiDAR earthworks and unusual soil signatures from satellite data.
        *   **Scenario C (High-Density Textual + Remote Sensing):** Identify areas with a high spatial density of relevant textual entities (e.g., multiple mentions of "settlement," "artifacts," "mounds" within a certain radius). Then, analyze remote sensing data within these high-density textual zones for corresponding features.
            *   *Example:* An area where several historical accounts mention "large settlements" and resource exploitation, and which also shows extensive subtle earthworks in LiDAR.
        *   **Scenario D (Pattern Congruence):**
            *   *Example:* A textual description of "ring villages" is used to search for circular/annular patterns in both LiDAR (e.g., ring-shaped earthworks) and satellite imagery (e.g., circular vegetation patterns) in the plausible geographic region.
    3.  **PIZ Delineation:** The output of these overlay operations will be new polygons representing the PIZs. Each PIZ will inherit attributes from the parent features that contributed to its creation (e.g., type of LiDAR anomaly, type of spectral signature, keywords from textual mention).

### 1.3. Handling Spatial Uncertainty and Varying Resolutions

*   **Spatial Uncertainty (Textual Data):**
    *   Use variable buffer sizes for geocoded textual mentions based on the specificity of the description (e.g., a named site might get a smaller buffer than a general regional description).
    *   Attribute PIZs with the source and estimated uncertainty of textual information.
*   **Varying Resolutions (Remote Sensing):**
    *   **Prioritization:** Higher resolution data (e.g., LiDAR for topography, high-res satellite for specific feature outlines) might be given more weight in defining the precise boundaries of a PIZ if there's a general agreement from lower-resolution data.
    *   **Scale of Analysis:** Features visible at different scales will be considered. For example, a large-scale vegetation anomaly (Sentinel) might contain smaller, specific topographic features (LiDAR). The PIZ would encompass the broader area, with internal "hotspots."
    *   **Generalization:** For initial PIZ generation, features from higher-resolution data might be slightly generalized (e.g., simplified polygons) to facilitate robust overlaps with lower-resolution data without creating excessive numbers of tiny PIZs.
    *   **Feature Presence vs. Precise Boundary:** The goal is to identify zones of interest. The exact boundary of an archaeological site within a PIZ often cannot be determined solely from this level of analysis.

## 2. Predictive Model / Scoring System Design

Once PIZs are delineated, a system will be needed to rank or score them based on the accumulated evidence to prioritize further investigation. A heuristic (knowledge-based) scoring system is proposed as the primary approach due to the likely scarcity of comprehensive, labeled training data for a supervised machine learning model across the vast and diverse Amazon.

### 2.1. Heuristic Scoring System

This system will assign scores to PIZs based on predefined parameters and weights reflecting the strength, type, and convergence of evidence.

*   **Parameters for Scoring:**
    1.  **Number of Confirming Data Types:**
        *   Score: Higher if evidence from 2 or 3 data types (LiDAR, Satellite, Textual) converges within the PIZ.
        *   *Example:* LiDAR anomaly only (1 point), LiDAR + Satellite (3 points), LiDAR + Satellite + Textual (5 points).
    2.  **Clarity/Strength of LiDAR Features:**
        *   Qualitative assessment (e.g., Low, Medium, High clarity) based on EDA.
        *   *Example:* Vague topographic anomaly (1 pt), Clear geometric earthwork (3 pts).
    3.  **Significance of Satellite Signatures:**
        *   Type of anomaly (e.g., subtle vegetation stress vs. distinct geometric clearing).
        *   Intensity/contrast of the anomaly.
        *   *Example:* Faint NDVI variation (1 pt), Strong, unexplained geometric pattern in multiple indices (3 pts).
    4.  **Relevance/Reliability of Textual Mentions:**
        *   Directness of archaeological reference (e.g., "ancient earthworks" vs. general "old village").
        *   Specificity of location (e.g., named site vs. regional mention).
        *   Source type (e.g., archaeological report vs. colonial diary – consider potential biases).
        *   *Example:* Vague folklore reference (0.5 pts), Direct mention of ruins by an archaeologist (3 pts).
    5.  **Rarity/Uniqueness of Features:**
        *   How distinct are the observed remote sensing features from the surrounding natural landscape or modern anthropogenic patterns?
        *   *Example:* Common fluvial terrace (0 pts), Highly unusual geometric earthwork pattern (2 pts).
    6.  **Size/Extent of Potential Site:**
        *   Larger contiguous areas of anomalies might indicate more significant sites, but small, distinct features are also important. This needs careful balancing.
        *   *Example:* Small isolated mound (1 pt), Large complex of earthworks (3 pts).
    7.  **Proximity to Key Resources (if derivable):**
        *   Proximity to historical water sources (from NDWI, DTMs, or textual mentions).
        *   Proximity to areas with soil signatures like "terra preta" (if identifiable).
        *   *Example:* Close to perennial river (1 pt).

*   **Assigning Weights:**
    *   Weights will be assigned to each parameter category based on their perceived importance in indicating archaeological potential. This will be subjective but guided by archaeological domain knowledge and the reliability of each data type.
    *   *Example Weights:* Convergence (x3), LiDAR Clarity (x2), Satellite Sig. (x2), Textual Rel. (x1.5), Uniqueness (x1), Size (x1).
*   **Calculating PIZ Score:**
    *   `PIZ_Score = (Parameter1_Score * Weight1) + (Parameter2_Score * Weight2) + ...`
*   **Output:** A ranked list of PIZs, with their scores and a summary of the evidence contributing to the score.

### 2.2. Machine Learning Approach (Conceptual - Secondary)

While the heuristic approach is primary, if a substantial and representative dataset of *known and verified* archaeological sites (both positive and negative examples – i.e., areas confirmed to have no sites) becomes available *and* these sites can be characterized using the same features derived from our LiDAR, Satellite, and Textual data processing pipelines, a supervised ML model could be considered.

*   **Potential Models:** Random Forest, Logistic Regression, Support Vector Machines, Gradient Boosting Machines.
*   **Features:**
    *   **LiDAR-derived:** Mean elevation, slope, aspect, SVF, LRM values within PIZ; presence/density of specific feature types (mounds, lines); textural features from DTM/hillshade.
    *   **Satellite-derived:** Mean/median values of various spectral indices (NDVI, NDWI, BSI, etc.) within PIZ; textural features from selected bands/indices; presence/type of detected anomalies.
    *   **Textual-derived:** Binary flags for mention of specific keywords (earthwork, settlement, etc.); density of relevant named entities; proximity to geocoded textual mentions.
    *   **Combined:** Number of data types confirming, distance metrics between features from different sources.
*   **Challenges:**
    *   **Training Data Scarcity & Bias:** The biggest challenge. Known sites are often clustered in researched areas, leading to spatial bias. True negative samples are hard to confirm.
    *   **Data Imbalance:** Far more non-site areas than site areas. Requires techniques like oversampling/undersampling (e.g., SMOTE) or cost-sensitive learning.
    *   **Feature Representation:** Converting diverse data into meaningful, comparable numerical features for the model.
    *   **Spatial Autocorrelation:** Sites are often clustered, which can violate model assumptions of independent samples. Requires spatial cross-validation techniques.
    *   **Generalizability:** A model trained in one part of the Amazon might not generalize well to other areas with different environmental conditions or archaeological manifestations.

*Given these complexities, the heuristic scoring system is the more pragmatic approach for this project's scope unless a surprisingly rich training dataset is provided.*

## 3. Role of OpenAI Models in Site Prediction/Plausibility

OpenAI models (e.g., GPT-4.1) can act as a "reasoning engine" or "expert assistant" to help refine hypotheses about PIZs, particularly those with complex or ambiguous evidence.

*   **Assessing Plausibility & Generating Hypotheses:**
    *   **Input to Model:** A structured summary of evidence for a high-scoring PIZ.
        *   *Example:* "PIZ #123 (Coordinates: X,Y): Evidence: 1. LiDAR shows multiple linear mounds (approx. 1-2m high, 50-100m long) oriented E-W. 2. Sentinel-2 NDVI shows slightly lower values over these linear features compared to adjacent forest. 3. Textual analysis of 18th-century Document X mentions 'raised causeways used for travel during floods' by the 'Yanoama people' in a region ~5km north of this PIZ."
    *   **Prompt to Model:**
        *   "Based on this combined evidence, assess the archaeological plausibility of this PIZ. What type of archaeological site or features might this represent? What are common characteristics of such sites in the Amazonian context? Are there any alternative (non-archaeological) explanations for these features?"
        *   "What further investigation steps (using the available data types or suggesting new ones) would you recommend to clarify the nature of this PIZ?"
    *   **Output:** A textual assessment from the model, providing a qualitative judgment, potential interpretations, and research questions. This can help human analysts think through the evidence.
*   **Generating Descriptive Summaries:**
    *   For top-ranked PIZs, use the model to generate concise, human-readable summaries of the evidence. This is useful for reports or for presenting candidate sites to other researchers.
    *   **Input:** Structured list of features and scores for a PIZ.
    *   **Prompt:** "Generate a 150-word descriptive summary for a potential archaeological site candidate, highlighting the key evidence from LiDAR, satellite imagery, and textual sources."
*   **Identifying Conflicting Evidence or Gaps:**
    *   The model could be prompted to identify any conflicting pieces of evidence or data gaps for a PIZ that might weaken the hypothesis or suggest specific data to acquire/analyze next.

*The LLM's role is not to make definitive predictions but to assist in sense-making, hypothesis generation, and articulating the evidence for human review.*

## 4. Verification Strategies

For the top candidate sites/PIZs identified by the scoring system, verification using at least two independent methods is crucial. Verification aims to increase confidence in the archaeological nature of a PIZ, not necessarily to provide definitive proof (which often requires fieldwork).

1.  **Cross-Data Corroboration (Primary Internal Method):**
    *   **Description:** If a PIZ was primarily identified or scored highly due to features from one data type (e.g., LiDAR), rigorously re-examine the other available data types (Satellite, Textual) specifically for that exact location, looking for subtle or previously overlooked corroborating evidence.
    *   **Example:** A LiDAR anomaly is re-inspected on all available Sentinel-2 bands, indices, and time-series data. Textual corpus is queried for any keywords related to the anomaly's location or morphology.
    *   **Strength:** Uses existing processed data; internal to the project.

2.  **Detailed Multi-Source Re-Analysis (Enhanced Internal Method):**
    *   **Description:** For a top PIZ, conduct a focused, small-scale re-analysis. This might involve re-running processing steps with different parameters for that specific micro-AOI (e.g., different DTM interpolation, more sensitive spectral enhancement, alternative OCR for a specific text mentioning the area).
    *   **Example:** If a PIZ shows faint linear features, re-process LiDAR for that specific tile using different ground classification or DTM generation parameters; apply specialized edge-detection or texture algorithms to satellite imagery for that specific zone.
    *   **Strength:** Deepens analysis of existing data; allows for methodological refinement for specific targets.

3.  **Historical Map Overlay & Analysis:**
    *   **Description:** Acquire and georeference relevant historical maps (from sources like David Rumsey Collection, national libraries, etc.). Overlay the PIZ location on these maps to see if any historical features (settlements, paths, old river courses, missions) are marked at or near the location.
    *   **Example:** A PIZ aligns with a "village" symbol or a "Rapids of X" on a 1750s map.
    *   **Strength:** Provides historical context; can directly confirm past occupation or landscape features if present on maps. Accuracy depends on map quality and georeferencing precision.

4.  **Comparative Morphological/Pattern Analysis (Literature-Based):**
    *   **Description:** Research documented archaeological sites in similar Amazonian environments (e.g., várzea, interfluvial, upland forests). Compare the morphology, size, layout, and environmental setting of features within the PIZ to these known sites.
    *   **Example:** If a PIZ contains ring-like earthworks, compare their dimensions and arrangement to known Amazonian ring villages. If it contains linear mounds, compare to known causeway systems or raised field complexes.
    *   **Strength:** Grounds PIZ interpretation in existing archaeological knowledge; helps assess if features fit known patterns. Requires literature review.

5.  **Consulting External Databases/Experts (Ethical/Permissibility Considerations):**
    *   **Description:** If ethically permissible and allowed by competition rules, check the PIZ location against publicly accessible (non-competition provided) archaeological site databases or gazetteers for the region to see if it corresponds to a known (but perhaps not widely published) site. *This must be done with extreme caution regarding data licensing and competition rules.*
    *   Seeking general advice from domain experts on the *types* of features being observed (without revealing specific PIZ locations if prohibited) might also be a form of conceptual verification.
    *   **Strength:** Can quickly confirm known sites; expert opinion can guide interpretation. **Weakness:** Highly dependent on external factors and permissions.

6.  **Environmental/Simulation Modeling (Contextual Verification):**
    *   **Description:** For certain types of hypothesized sites, environmental modeling can assess suitability.
        *   *Hydrological modeling:* If features are thought to be canals or related to water management, model local hydrology from DTMs.
        *   *Visibility/Intervisibility analysis:* If features are thought to be defensive or ceremonial, analyze lines of sight from/to the PIZ.
        *   *Resource proximity modeling:* Model proximity to historically important resources (water, specific soils, defensible terrain).
    *   **Strength:** Assesses if the environmental context fits the hypothesized function of the site.

**Choice of Verification Methods:** The selection of methods will depend on the nature of the PIZ, the primary data that identified it, and the available resources/time. A combination (e.g., Cross-Data Corroboration + Historical Map Overlay + Comparative Morphological Analysis) would be robust.

This strategy aims to provide a systematic and multi-faceted approach to identifying, prioritizing, and increasing confidence in potential archaeological sites within the Amazon, leveraging the diverse data sources and analytical techniques developed throughout the project.The strategy document `SITE_PREDICTION_VERIFICATION_STRATEGY.md` has been created.

It covers the following key areas as requested:

1.  **Methodology for Integrating EDA Insights:**
    *   Details how findings from LiDAR (topographic anomalies), Satellite (spectral/vegetation patterns), and Textual EDA (geocoded names, descriptions) will be spatially represented.
    *   Proposes methods for creating "Potential Interest Zones" (PIZs) through GIS overlay operations based on convergence of evidence (e.g., LiDAR + Satellite, Textual + Remote Sensing, High-density Textual + Remote Sensing, Pattern Congruence).
    *   Discusses handling spatial uncertainty (buffering, attributing uncertainty) and varying data resolutions (prioritization, scale of analysis, generalization).

2.  **Predictive Model/Scoring System Design:**
    *   Primarily outlines a **Heuristic Scoring System** for ranking PIZs. This includes defining parameters (number of confirming data types, clarity/strength of features from each source, textual relevance, uniqueness, size) and assigning weights to them.
    *   Conceptually discusses a **Machine Learning Approach** (e.g., Random Forest) as a secondary option, outlining potential features and significant challenges (training data scarcity, imbalance, feature representation, generalizability), concluding the heuristic system is more pragmatic for this project.

3.  **Role of OpenAI Models in Site Prediction/Plausibility:**
    *   Suggests using OpenAI models (e.g., GPT-4.1) to:
        *   Assess the archaeological plausibility of PIZs by feeding them summaries of evidence and asking for interpretations or further investigation steps.
        *   Generate descriptive summaries for high-potential candidate sites.
        *   Help identify conflicting evidence or data gaps.

4.  **Verification Strategies:**
    *   Proposes several independent methods for verifying top candidate PIZs, including:
        *   Cross-Data Corroboration (detailed re-examination of other data layers for a PIZ).
        *   Detailed Multi-Source Re-Analysis (re-processing data with different parameters for the specific PIZ).
        *   Historical Map Overlay & Analysis.
        *   Comparative Morphological/Pattern Analysis (literature-based comparison with known sites).
        *   Consulting External Databases/Experts (with ethical and rule-based caveats).
        *   Environmental/Simulation Modeling (hydrology, visibility, resource proximity).

The document provides a comprehensive strategy for moving from EDA insights to a prioritized list of candidate sites and their subsequent verification.
