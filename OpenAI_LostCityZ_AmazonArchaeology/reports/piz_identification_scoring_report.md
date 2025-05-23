# PIZ Identification and Scoring - Report

## 1. Introduction

This report details the initial system implemented for identifying Potential Interest Zones (PIZs) and scoring them based on multi-source evidence. This work aligns with the `SITE_PREDICTION_VERIFICATION_STRATEGY.md` and utilizes conceptual outputs from the Phase 3 Exploratory Data Analysis (EDA) notebooks for LiDAR, satellite, and textual data.

The primary tool for this implementation is the Jupyter Notebook: `notebooks/piz_identification_scoring.ipynb`.

The core objectives of this system are:
*   To systematically integrate findings from diverse data sources.
*   To define geographically specific zones (PIZs) that warrant further investigation.
*   To rank these PIZs using a configurable heuristic scoring mechanism.
*   To outline how advanced AI models (like OpenAI's GPT series) can be conceptually integrated for plausibility assessment of high-scoring PIZs.

## 2. Methodology

### 2.1. Integration of EDA Outputs

The system is designed to work with outputs from the EDA phase. For the current implementation in `piz_identification_scoring.ipynb`, these EDA outputs were represented as placeholder/simulated GeoDataFrames. In a full workflow, these would be populated from actual EDA results:

*   **LiDAR Anomalies:**
    *   **Source:** Findings from `lidar_eda.ipynb` (e.g., coordinates/polygons of mounds, linear earthworks, distinct topographic signatures).
    *   **Representation:** A GeoDataFrame where each entry has a geometry (Point or Polygon) and attributes like `lidar_clarity` (e.g., a 1-5 scale indicating how clearly an anomaly is defined) and `lidar_feature_type` (e.g., 'mound', 'linear_depression').
*   **Satellite Anomalies:**
    *   **Source:** Findings from `satellite_eda.ipynb` (e.g., regions with unusual NDVI, geometric vegetation patterns, distinct soil signatures from indices like BSI).
    *   **Representation:** A GeoDataFrame with geometries and attributes like `satellite_significance` (1-5 scale for anomaly strength/distinctness) and `satellite_anomaly_type` (e.g., 'ndvi_low_circular', 'veg_pattern_geometric').
*   **Textual Mentions:**
    *   **Source:** Geocoded entities or regions of interest from `textual_eda_openai.ipynb` (e.g., textually mentioned settlements, resource areas, coordinates derived from descriptions).
    *   **Representation:** A GeoDataFrame with point geometries and attributes like `textual_reliability` (1-5 scale for confidence in geocoding/relevance) and `textual_mention_type` (e.g., 'settlement_described', 'resource_area').
*   **Area of Interest (AOI):** The overall AOI boundary is loaded from `config.ini` (BBOX or GeoJSON) and used for context and spatial operations. All spatial data is assumed to be in or reprojected to a consistent `TARGET_PROJECTED_CRS` defined in the configuration.

### 2.2. PIZ Definition

The notebook implements an initial PIZ definition strategy based on **Proximity/Overlap of Anomalies**:

1.  **Buffering:** A buffer distance (e.g., 200 meters, configurable) is applied to the geometries of individual anomalies from each data source (LiDAR, Satellite, Textual). Textual mentions can optionally have a larger buffer to account for lower spatial precision.
2.  **Aggregation:** All buffered geometries are combined into a single collection.
3.  **Dissolving Overlaps:** Overlapping buffers are dissolved to form larger, contiguous zones. These dissolved zones represent initial candidate areas where multiple pieces of evidence might be spatially related.
4.  **Characterization:** Each dissolved zone is then analyzed to identify which original (unbuffered) anomalies from LiDAR, Satellite, and Textual sources intersect it. This step determines:
    *   The number of unique data source types contributing to the zone (`num_sources`).
    *   A list of specific features/anomalies from each source type that fall within the zone.
    *   The maximum clarity/significance/reliability scores from the features within the zone for each data type.
5.  **PIZ Finalization:** Zones that meet a minimum criterion (e.g., evidence from at least one or, more stringently, two source types) are designated as PIZs and assigned a unique `piz_id`.

A conceptual **Gridding Approach** was also mentioned in the notebook as an alternative: dividing the AOI into cells and scoring cells based on the density/combination of anomalies within them. However, the buffer/overlap method was implemented as it's more directly driven by the detected features.

### 2.3. Heuristic Scoring System

A heuristic scoring system, as outlined in `SITE_PREDICTION_VERIFICATION_STRATEGY.md`, was implemented to rank the identified PIZs.

*   **Scoring Parameters & Weights:**
    The score for each PIZ is calculated based on a weighted sum of factors:
    *   `num_sources`: Number of unique data types (LiDAR, Satellite, Textual) contributing evidence to the PIZ. (Weight example: 3.0)
    *   `lidar_clarity_max`: Maximum clarity score of any LiDAR anomaly within the PIZ. (Weight example: 2.0)
    *   `satellite_significance_max`: Maximum significance score of any satellite anomaly within the PIZ. (Weight example: 2.0)
    *   `textual_reliability_max`: Maximum reliability score of any textual mention within the PIZ. (Weight example: 1.5)
    *   `proximity_to_water`: (Optional bonus) If the PIZ is near a known water source. (Weight example: 0.5)
    *   `uniqueness_factor`: (Placeholder) Could be used to score based on the rarity of observed patterns.

    These weights are configurable and can be tuned based on domain expertise or iterative refinement.

*   **Calculation:** Each PIZ receives a score:
    `Score = (num_sources * W_num_sources) + (lidar_clarity_max * W_lidar) + ...`

*   **Output:** The notebook produces a GeoDataFrame of PIZs, sorted by their scores in descending order, allowing for prioritization. Key attributes like `piz_id`, `score`, `contributing_sources`, and descriptions of intersecting features are included. This table can be saved as GeoJSON and CSV.

### 2.4. Visualization

The notebook includes steps to visualize:
*   The AOI boundary.
*   The locations of the original (simulated) LiDAR, Satellite, and Textual anomalies.
*   The identified PIZs, typically color-coded by their calculated score, to provide a spatial overview of high-priority areas.
*   Labels for PIZ IDs and their scores on the map.

These visualizations are saved as PNG files in the `eda_outputs/piz/` directory.

## 3. Example of a Scored PIZ List (Hypothetical)

Based on the placeholder data used in the notebook, a hypothetical sorted PIZ list might look like this:

| piz_id | score | num_sources | contributing_sources   | all_intersecting_features_desc                                                                                                |
| :----- | :---- | :---------- | :--------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| 0      | 24.5  | 3           | lidar, satellite, textual | L: point_mound (Clarity: 4); S: ndvi_low_circular (Sig: 3); T: settlement_possible_ruins (Rel: 4)                             |
| 1      | 10.0  | 1           | lidar                  | L: linear_earthwork (Clarity: 5)                                                                                             |
| 2      | 8.0   | 1           | satellite              | S: veg_pattern_geometric (Sig: 4)                                                                                             |
| 3      | 3.0   | 1           | textual                | T: general_region_activity_X (Rel: 2)                                                                                         |

*(Note: Actual scores and descriptions depend on the input anomalies and scoring weights.)*

## 4. OpenAI for Plausibility Assessment (Conceptual Integration)

The notebook demonstrates how to structure prompts for an OpenAI model (e.g., GPT-4) to assess the archaeological plausibility of top-scoring PIZs.

*   **Prompt Formulation:** For a given PIZ, a detailed prompt is constructed, including:
    *   PIZ ID and approximate coordinates.
    *   The heuristic score and number of contributing data source types.
    *   A summary of evidence from each source type (e.g., "LiDAR evidence: Max clarity score 4. Features include: point_mound.").
    *   Specific questions for the AI, such as:
        *   What type of archaeological site/features might this represent in an Amazonian context?
        *   Common characteristics of such sites?
        *   Alternative (non-archaeological) explanations?
        *   Aspects making the PIZ more/less plausible?
        *   Recommended further investigation steps.

*   **Purpose:** This conceptual integration shows how LLMs can act as a "reasoning assistant" to help human analysts interpret complex multi-source evidence, generate hypotheses, and identify gaps or conflicts in the data for a specific PIZ. Actual API calls were not implemented in this notebook phase but the prompt structure is provided.

## 5. Discussion: Heuristic Scoring, Tuning, and Limitations

*   **Heuristic Nature:** The scoring system is knowledge-driven and relies on subjective (but expert-informed) weights and parameter scores (e.g., manual clarity/significance scores for anomalies if not yet quantified). This is a pragmatic approach given the likely absence of extensive labeled training data for a supervised ML model.
*   **Tunability:** The weights and even the scoring parameters themselves are designed to be tunable. As the project progresses and verification feedback becomes available (Phase 4), these can be adjusted to improve the ranking accuracy.
*   **Simplicity vs. Complexity:** The current PIZ definition (buffer/overlap) is relatively simple. More complex spatial relationships or feature characteristics could be incorporated into the scoring (e.g., size of anomaly, orientation, specific keywords from text).
*   **Dependence on EDA Quality:** The quality of PIZs and their scores is highly dependent on the quality and comprehensiveness of the anomaly detection and characterization performed in the Phase 3 EDA notebooks. If EDA outputs are noisy or incomplete, the PIZ generation will inherit these limitations.
*   **Placeholder Data:** The current implementation uses placeholder anomalies. Integrating actual, diverse outputs from the EDA phase will be crucial for realistic testing and refinement. This involves standardizing the output formats from EDA notebooks (e.g., GeoJSONs with consistent attribute schemas).

## 6. Conclusion and Next Steps

The `piz_identification_scoring.ipynb` notebook provides a foundational system for integrating multi-source EDA findings to identify and rank Potential Interest Zones. The heuristic scoring mechanism offers a transparent and adaptable way to prioritize areas for further investigation. The conceptual integration of OpenAI for plausibility assessment further enriches the analytical toolkit.

**Key Next Steps:**

1.  **Integrate Real EDA Outputs:** Replace placeholder data with actual outputs from `lidar_eda.ipynb`, `satellite_eda.ipynb`, and `textual_eda_openai.ipynb`. This will require defining and adhering to clear data schemas for these outputs.
2.  **Refine PIZ Definition Logic:** Experiment with different buffering strategies, spatial clustering techniques (e.g., DBSCAN), or the gridding approach to optimize PIZ delineation.
3.  **Iteratively Tune Scoring System:** Adjust weights and scoring parameters based on archaeological domain knowledge and, eventually, feedback from verification efforts.
4.  **Develop Quantitative Anomaly Attributes:** Where possible, replace manual scores (e.g., "clarity") from EDA with quantifiable metrics (e.g., statistical significance of NDVI deviation, geometric properties of LiDAR features).
5.  **Expand Feature Set for Scoring:** Consider incorporating additional spatial context (e.g., proximity to different types of water bodies, terrain ruggedness, soil types) if relevant data layers are available.
6.  **Operationalize OpenAI Interaction:** If deemed valuable, automate the process of sending prompts for top PIZs to OpenAI and storing the textual assessments.

This system provides a crucial bridge between exploratory analysis and targeted investigation, forming a key component of the overall strategy to discover and verify potential archaeological sites in the Amazon.The Jupyter Notebook `notebooks/piz_identification_scoring.ipynb` was created in the previous turn. It outlines the structure for PIZ identification and scoring, including loading (placeholder) EDA outputs, defining PIZs through buffer/overlap, implementing a heuristic scoring system, demonstrating conceptual OpenAI prompt formulation, and visualizing results.

The task also requires a markdown report, `piz_identification_scoring_report.md`. I have just created this report.

The report summarizes:
1.  **Methodology:**
    *   How EDA outputs (LiDAR, Satellite, Textual) are conceptually integrated (using placeholder GeoDataFrames in the notebook).
    *   The PIZ definition process (buffer-and-overlap of anomalies).
    *   The heuristic scoring system (parameters, weights, calculation).
    *   Visualization of PIZs.
2.  **Example Scored PIZ List:** A hypothetical table showing ranked PIZs with scores and contributing evidence.
3.  **OpenAI for Plausibility Assessment:** How prompts are structured to leverage LLMs for assessing top PIZs.
4.  **Discussion:** Covers the heuristic nature of the scoring, tunability, limitations (dependency on EDA quality, placeholder data), and overall system design.
5.  **Conclusion and Next Steps:** Summarizes the achievement and outlines future refinements like integrating real EDA outputs, tuning the scoring system, and operationalizing OpenAI interaction.

Both deliverables, the notebook (`piz_identification_scoring.ipynb`) and the report (`piz_identification_scoring_report.md`), are now complete as per the subtask requirements. The notebook provides the "how-to" with code, and the report explains the "what and why," including hypothetical examples to illustrate the process.
