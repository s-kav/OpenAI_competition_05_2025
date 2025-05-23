# Guidelines for Evidence Compilation and Insight Generation for Top PIZs

## 1. Introduction

**Purpose:** This document provides guidelines and a template for systematically compiling all gathered evidence for each of the top N Potential Interest Zones (PIZs) selected after the Phase 4 verification process. The compiled evidence will then be used, with the assistance of OpenAI models, to synthesize information, generate coherent narratives, and derive potential historical insights for each candidate site.

This process aims to create a rich, evidence-based dossier for each top PIZ, facilitating a deeper understanding of its archaeological potential and informing any subsequent research or fieldwork planning.

## 2. Candidate Site Dossier Template

For each top candidate PIZ, a "Site Dossier" will be created. This can be a dedicated markdown file (e.g., `PIZ_ID_XXX_Dossier.md`) or a structured section within a larger project document/database. The use of markdown is encouraged for its flexibility in combining text, links, and embedded or linked images.

Below is the proposed template structure:

---

### Site Dossier: PIZ `[PIZ_ID_XXX]`

**Date Compiled:** `YYYY-MM-DD`
**Compiler(s):** `[Name(s)]`

**1. PIZ Identifier & Location:**
    *   **PIZ ID:** `[Unique PIZ Identifier from Phase 4 Scoring]`
    *   **Approximate Centroid Coordinates:**
        *   Projected CRS: `[e.g., EPSG:31980, X: 123456, Y: 9876543]`
        *   Geographic (Lat/Lon, WGS84): `[e.g., Latitude: -2.5678, Longitude: -60.1234]`
    *   **Link to Interactive Map/GIS Layer:** `[e.g., Link to a GeoJSON view or specific map showing the PIZ boundary and context]`
    *   **General Location Description:** `[Brief textual description, e.g., "Located on an interfluvial bluff, approx. 2km east of the Rio Menor, within the broader Xingu watershed."]`

**2. Summary Score & Verification Overview (from Phase 4):**
    *   **Heuristic Score:** `[Score from piz_identification_scoring.ipynb]`
    *   **Rank:** `[Rank from piz_identification_scoring.ipynb]`
    *   **Key Contributing Factors to Score:** `[e.g., "High LiDAR clarity, convergence of 3 data sources (LiDAR, Satellite, Textual)"]`
    *   **Phase 4 Verification Summary:** `[Brief summary of verification methods applied and their overall outcome/confidence level, e.g., "Cross-data corroboration confirmed spatial alignment of LiDAR earthworks with vegetation anomalies. Comparative analysis suggests morphology consistent with small fortified villages."]`

**3. LiDAR Evidence:**
    *   **Description of Anomalies:**
        *   `[Detailed textual description of observed topographic features: e.g., "A series of three circular mounds, each approx. 15-20m in diameter and 1-1.5m in height, arranged in a triangular pattern. A linear depression, possibly a ditch or ancient path, runs along the western edge of the mound group."]`
    *   **Key Visualizations (Paths to Image Files):**
        *   Primary Hillshade (best illustrating features): `[e.g., ../eda_outputs/lidar/PIZ_XXX_dtm_hillshade_NW.png]`
        *   Slope Map highlighting features: `[e.g., ../eda_outputs/lidar/PIZ_XXX_dtm_slope.png]`
        *   Contour Map snippet: `[e.g., ../eda_outputs/lidar/PIZ_XXX_dtm_contours_display.png]`
        *   Other relevant DTM derivatives (SVF, LRM if generated): `[Path to image]`
        *   *(Embed key images directly or provide clear links if stored elsewhere)*
    *   **Measurements (if applicable):**
        *   Feature 1 (e.g., Mound A): Dimensions `[L x W x H]`, Area `[m^2]`, Orientation `[degrees from N]`
        *   Feature 2 (e.g., Linear Depression): Length `[m]`, Average Width `[m]`, Average Depth `[m]`
        *   *(Use a table or bullet points)*

**4. Satellite Imagery Evidence:**
    *   **Description of Spectral or Visual Anomalies:**
        *   `[Detailed textual description: e.g., "The area corresponding to the LiDAR mounds shows a subtle but persistent circular patch of lower NDVI (0.45) compared to surrounding forest (NDVI 0.7-0.8) across multiple dry season images. False color composite (NIR-R-G) depicts this area with a slightly darker red tone, suggesting altered vegetation composition or health."]`
    *   **Key Visualizations (Paths to Image Files):**
        *   True Color Composite snippet: `[e.g., ../eda_outputs/satellite/PIZ_XXX_true_color.png]`
        *   False Color (Vegetation) Composite snippet: `[e.g., ../eda_outputs/satellite/PIZ_XXX_false_color_veg.png]`
        *   Key Spectral Index Map (e.g., NDVI): `[e.g., ../eda_outputs/satellite/PIZ_XXX_ndvi.png]`
        *   *(Embed key images directly or provide clear links)*
    *   **Temporal Changes (if observed and relevant):**
        *   `[Description of any significant changes observed over time, e.g., "Comparison of 2018 and 2023 imagery shows the NDVI anomaly has remained stable, suggesting it's not recent agricultural clearing."]`

**5. Textual Evidence:**
    *   **Relevant Excerpts (with Citations):**
        *   Document 1 (`[Source Document Name/ID]`): `["Quote the relevant passage(s) here..."]` (Page `[X]`)
        *   Document 2 (`[Source Document Name/ID]`): `["Another relevant quote..."]` (URL/DOI `[Y]`)
    *   **Named Entity Recognition (NER) Output Summary (for this specific PIZ's vicinity):**
        *   Place Names: `[List of relevant geocoded place names from textual_eda_openai.ipynb that fall within or near the PIZ]`
        *   Dates/Time Periods: `[List of relevant dates]`
        *   Indigenous Groups: `[List of relevant groups]`
        *   Settlement Structures/Features Mentioned: `[List of terms like 'earthwork', 'village', etc.]`
        *   Resources Mentioned: `[List of relevant resources]`
    *   **OpenAI-Assisted Summary of Textual Information (Specific to this PIZ - *see section 4 below*):**
        *   `[This section will contain a concise summary generated with AI assistance, focusing on textual information directly pertinent to this PIZ's location and characteristics.]`

**6. Spatial Overlays and Convergence of Evidence:**
    *   **Description of Spatial Alignment:**
        *   `[Detailed textual description of how features from different data sources align spatially. e.g., "The circular NDVI anomaly (Satellite) directly overlays the largest LiDAR-identified mound. A historical text mentions a 'chief's village' located near a 'prominent hill' which aligns with the geocoded text point buffer intersecting this PIZ."]`
    *   **Key Map Showing Overlay of Evidence Layers (Path to Image File):**
        *   `[e.g., ../eda_outputs/piz/PIZ_XXX_evidence_overlay_map.png]`
        *   *(This map should clearly show the PIZ boundary with LiDAR features, key satellite anomalies, and relevant textual mention points/buffers overlaid.)*
    *   **Table of Converging Evidence (Optional but Recommended):**

        | Feature ID/Location | Evidence Type | Description of Evidence                                  | Confidence/Clarity | Notes on Convergence                                                                 |
        | :------------------ | :------------ | :------------------------------------------------------- | :----------------- | :----------------------------------------------------------------------------------- |
        | Mound Complex A     | LiDAR         | Three circular mounds, 15-20m diameter, 1-1.5m high      | High               | Overlaps with Satellite Anomaly #1 (low NDVI)                                        |
        | Mound Complex A     | Satellite     | Circular low NDVI patch (0.45)                           | Medium             | Spatially coincident with LiDAR mounds                                               |
        | PIZ Vicinity        | Textual       | "Chief's village on hill" (Doc X, geocoded point near PIZ) | Medium (geocoding) | Supports presence of significant settlement in area containing mounds                |
        | Linear Feature B    | LiDAR         | 50m linear depression, 0.5m deep                         | Medium             | No direct satellite or current textual corroboration, but morphology suggests canal. |

**7. AI-Generated Synthesis and Insights (from Section 4 prompts below):**
    *   **7.1. Synthesized Narrative of Potential Archaeological Nature:**
        *   `[Output from OpenAI model based on prompt in section 4.1]`
    *   **7.2. Potential Historical Interpretations and New Hypotheses:**
        *   `[Output from OpenAI model based on prompt in section 4.2]`
    *   **7.3. Key Research Questions Raised:**
        *   `[List of questions, potentially derived from AI output or human analysis of the dossier]`

**8. Overall Assessment and Confidence:**
    *   **Summary Interpretation:** `[Human expert's brief interpretation of all compiled evidence.]`
    *   **Confidence in Archaeological Potential:** `[High/Medium/Low - with justification]`
    *   **Remaining Ambiguities/Questions:** `[List any unresolved issues or areas needing further clarification.]`

**9. Recommendations for Next Steps:**
    *   `[e.g., "Recommend for targeted high-resolution remote sensing.", "Prioritize for simulated fieldwork planning.", "Requires further specific textual research on Group X."]`

---

## 3. Overall Documentation of Measurements, Overlays, and Convergence

Systematic documentation is key to ensuring clarity and reproducibility.

*   **Measurements:**
    *   All measurements (size, area, length, height/depth of features) should be recorded with units (e.g., meters).
    *   The method of measurement should be noted (e.g., "derived from DTM profile in QGIS," "estimated from pixel count on 10m Sentinel imagery").
    *   Store tabular data of measurements in CSV files linked within the dossier or directly in tables in the markdown.
*   **Spatial Overlays:**
    *   Create dedicated maps (exported as PNG or similar) for each PIZ, clearly showing the spatial relationships between different evidence layers (LiDAR features, satellite anomalies, textual mention buffers, PIZ boundary).
    *   Use consistent symbology and clear legends. Annotations on these maps should highlight key areas of convergence.
    *   These maps should be saved in a structured way (e.g., `eda_outputs/piz/PIZ_ID_XXX_evidence_map.png`) and referenced in the dossier.
*   **Convergence of Evidence:**
    *   Explicitly describe where and how different data types support each other in the "Spatial Overlays and Convergence" section of the dossier.
    *   The optional "Table of Converging Evidence" (shown in the template) provides a structured way to list specific features within the PIZ and detail how each data source contributes to understanding that feature.

## 4. OpenAI Model Integration for Synthesis and Insight

Once the evidence for a PIZ is compiled in its dossier (Sections 1-6), OpenAI models (e.g., GPT-4.1, or the latest available high-reasoning model) will be used to assist in synthesizing this information and generating higher-level insights.

### 4.1. Evidence Synthesis Prompting Strategy

*   **Objective:** To generate a concise, coherent narrative describing the potential archaeological nature of the site based on the compiled multi-source evidence.
*   **Input Data for Prompt:** A condensed summary of the key findings from the dossier's sections on LiDAR, Satellite, Textual, and Verification evidence for that specific PIZ. This summary should be factual and avoid premature interpretation where possible.
*   **Example Prompt Structure:**

    ```
    System Message: You are an AI assistant specializing in archaeological data synthesis and interpretation, with knowledge of Amazonian archaeology. Your task is to create a coherent narrative from multi-source evidence.

    User Message:
    "Synthesize the following compiled evidence for Potential Interest Zone (PIZ) [PIZ_ID_XXX], located at approximately [Coordinates in Lat/Lon and Projected CRS], to describe its potential archaeological nature and significance. Focus on integrating the findings into a descriptive narrative.

    Evidence Summary:
    1.  **Overall PIZ Score & Verification:** [e.g., Heuristic Score: 85/100. Phase 4 Verification: Strong confidence from cross-data corroboration and comparative morphological analysis.]
    2.  **LiDAR Evidence:** [e.g., "Multiple distinct circular mounds (15-20m diameter, 1-2m high) and a linear depression (50m long, 0.5m deep) are clearly visible. Key visualizations confirm these are not obvious natural formations."]
    3.  **Satellite Imagery Evidence:** [e.g., "The area of the LiDAR mounds corresponds to a persistent circular patch of low NDVI (0.45) in Sentinel-2 imagery, distinct from surrounding forest (NDVI 0.7-0.8). No modern activity is visible in true color."]
    4.  **Textual Evidence (if any):** [e.g., "A 1785 historical account mentions a 'fortified village of the Araware people' located on a 'prominent series of hills near the Black River bend'. Geocoded estimates place this mention within a 1km buffer of the PIZ. NER identified 'Araware people', 'fortified village', 'hills', 'Black River bend'."]
    5.  **Spatial Convergence:** [e.g., "The LiDAR mounds, low NDVI patch, and the buffer of the textual mention for the 'Araware village' all show significant spatial overlap within this PIZ."]

    Based on this evidence, please provide:
    a) A concise narrative (approx. 200-300 words) describing the potential archaeological site, its key features, and its environmental setting.
    b) An assessment of the strength of the combined evidence pointing towards an anthropogenic origin.
    c) Any immediate observations about the potential cultural affiliation or function of the site based purely on the provided evidence synthesis."
    ```

### 4.2. Historical Insight Generation Prompting Strategy

*   **Objective:** To leverage the LLM's broader knowledge base (while being mindful of its limitations) to suggest potential historical interpretations, new hypotheses, or research questions that arise from the synthesized evidence.
*   **Input Data for Prompt:** The synthesized narrative generated in step 4.1 (or the evidence summary itself if preferred).
*   **Example Prompt Structure:**

    ```
    System Message: You are an AI assistant with expertise in Amazonian archaeology, anthropology, and historical ecology. Your task is to generate novel hypotheses and research questions based on summarized archaeological evidence.

    User Message:
    "Consider the following information regarding a Potential Interest Zone (PIZ_ID_XXX):
    [Insert either the AI-generated 'Synthesized Narrative' from 4.1 OR the detailed 'Evidence Summary' used in 4.1]

    Based on this information:
    1.  What are plausible historical or cultural interpretations for this site? (e.g., What type of settlement, defensive structure, agricultural feature, ceremonial site could it be? Consider known Amazonian cultures and patterns, but also be open to less common interpretations if the evidence is unusual).
    2.  What new hypotheses about past human activity, land use, or social organization in this specific region could be formulated based on the evidence for this site?
    3.  What specific research questions does this site raise that could guide future archaeological investigation (remote sensing, survey, or excavation if it were possible)?
    4.  Are there any apparent contradictions in the evidence, or aspects that are particularly puzzling or unique that warrant further thought?"
    ```

### 4.3. Output Management

*   **Recording:** The AI-generated narratives, interpretations, hypotheses, and research questions will be clearly labeled as "AI-Assisted Synthesis" or "AI-Generated Insights" and recorded directly into Section 7 ("AI-Generated Synthesis and Insights") of the respective PIZ Dossier.
*   **Review and Annotation:** All AI-generated text must be critically reviewed by human experts. Annotations, corrections, or alternative human interpretations should be added alongside the AI output. The AI's contribution is to assist and suggest, not to be the final authority.
*   **Iteration:** If the initial AI output is too generic or misses key points, the prompts will be refined and re-run. This iterative process is crucial.

By following these guidelines, each top PIZ will have a comprehensive dossier that not only compiles all available evidence but also leverages AI to help synthesize this information and spark deeper archaeological and historical understanding. This forms the basis for the final reporting and recommendations of the project.The document `EVIDENCE_COMPILATION_INSIGHT_GENERATION_GUIDELINES.md` has been created.

It includes the following sections as requested:

1.  **Introduction:**
    *   States the purpose: to systematically compile evidence for top N PIZs and use this, with AI assistance, to generate narratives and historical insights.

2.  **Candidate Site Dossier Template:**
    *   Proposes a structured markdown template for each PIZ dossier.
    *   Sections include:
        *   PIZ Identifier & Location (Coordinates, map link, description).
        *   Summary Score (from Phase 4).
        *   LiDAR Evidence (Description, key visualizations with paths, measurements).
        *   Satellite Imagery Evidence (Description, key visualizations with paths, temporal changes).
        *   Textual Evidence (Relevant excerpts, NER output summary, placeholder for OpenAI-assisted summary).
        *   Verification Results (Summary from Phase 4).
        *   Spatial Overlays and Convergence (Description of alignment, map path, optional table).
        *   AI-Generated Synthesis and Insights (Placeholders for outputs from prompts).
        *   Overall Assessment and Confidence (Human expert's summary).
        *   Recommendations for Next Steps.

3.  **Overall Documentation:**
    *   Briefly describes how to document measurements (with units, methods), spatial overlays (dedicated maps, consistent symbology, annotations), and the convergence of evidence (explicit descriptions, optional table).

4.  **OpenAI Model Integration for Synthesis and Insight:**
    *   **Evidence Synthesis Prompting Strategy:**
        *   Details the objective (generate coherent narrative).
        *   Specifies input data (condensed summary from dossier).
        *   Provides an example prompt structure for GPT-4.1 (or similar) to synthesize LiDAR, Satellite, Textual, and Verification evidence into a narrative, assess evidence strength, and make preliminary observations on function/affiliation.
    *   **Historical Insight Generation Prompting Strategy:**
        *   Details the objective (suggest new insights/hypotheses).
        *   Specifies input data (synthesized narrative or evidence summary).
        *   Provides an example prompt structure to ask the model for plausible historical/cultural interpretations, new hypotheses, research questions, and to identify contradictions or unique aspects.
    *   **Output Management:**
        *   How to record AI outputs in the dossier (labeled as AI-assisted).
        *   Emphasizes critical review and annotation by human experts.
        *   Mentions iterative prompt refinement.

The document provides a comprehensive set of guidelines and a practical template for Phase 5, focusing on systematic evidence compilation and the strategic use of AI for deeper analysis.
