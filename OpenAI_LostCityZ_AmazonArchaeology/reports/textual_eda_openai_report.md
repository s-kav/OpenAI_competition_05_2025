# Textual Data EDA with OpenAI Models - Report

## 1. Introduction

This report summarizes the initial Exploratory Data Analysis (EDA) performed on sample processed textual data using OpenAI language models (LLMs). The EDA was conducted using the `notebooks/textual_eda_openai.ipynb` Jupyter Notebook, following the strategy outlined in `EDA_FEATURE_ENGINEERING_STRATEGY.md`.

The primary goal was to demonstrate and evaluate the potential of using OpenAI models (specifically targeting GPT-3.5-turbo or similar via the OpenAI API) for several key NLP tasks relevant to Amazonian archaeology:
*   Named Entity Recognition (NER) for domain-specific entities.
*   Conceptual Topic Modeling (thematic summarization).
*   Relationship Extraction.
*   Geocoding assistance and disambiguation of place names.

The focus was on prompt engineering, interpreting model outputs, and understanding the practical application of these techniques for generating insights and features from textual data.

## 2. Data Used

*   **Input Data:** The EDA was designed to use processed `.txt` files located in the directory specified by `PROCESSED_TEXT_DIR` (e.g., `data/textual/processed/`).
*   **Sample Texts for this Report:** As actual processed files from Phase 2 were not available during this simulated execution, the notebook was set up to use three placeholder text samples if real data was insufficient. This report is based on the *expected outputs* from processing these placeholder texts:
    1.  `placeholder_colonial_diary_extract_processed.txt`: A fictional excerpt describing a journey up the Rio Negro, mentioning Indigenous groups, earthworks, and "El Dorado."
    2.  `placeholder_academic_paper_summary_processed.txt`: A fictional summary of an academic paper on settlements in the Upper Xingu, mentioning LiDAR, causeways, and ceramic evidence.
    3.  `placeholder_field_notes_short_processed.txt`: Fictional brief field notes mentioning a site, artifacts, and local accounts.
*   **Configuration:** All paths and parameters (including placeholders for the OpenAI API key setup) were managed via `scripts/satellite_pipeline/config.ini`.

## 3. OpenAI Model Tasks and Hypothetical Results

The `textual_eda_openai.ipynb` notebook structured the interaction with OpenAI models for the following tasks. We assume the OpenAI API client was initialized successfully (using an environment variable for the API key as recommended).

### 3.1. Named Entity Recognition (NER)

*   **Objective:** To extract predefined, domain-specific entities from the sample texts.
*   **Entity Types Defined:** `PLACE_NAME`, `ARCHAEOLOGICAL_SITE`, `INDIGENOUS_GROUP`, `DATE_TIME_PERIOD`, `SETTLEMENT_STRUCTURE`, `RESOURCE_MENTION`, `ARTIFACT`.
*   **Prompt Strategy:** The prompt instructed the model to identify these entities, provide the text segment, and return the output as a JSON object. It included an example of the desired JSON structure.
*   **Hypothetical Output (for `placeholder_colonial_diary_extract_processed.txt`):**
    ```json
    {
      "PLACE_NAME": ["Rio Negro", "Lake Parime"],
      "ARCHAEOLOGICAL_SITE": ["ancient earthworks", "geoglifos", "El Dorado"],
      "INDIGENOUS_GROUP": ["Manao"],
      "DATE_TIME_PERIOD": ["1750"],
      "SETTLEMENT_STRUCTURE": ["large villages", "extensive fields of manioc", "mounds"],
      "RESOURCE_MENTION": ["manioc", "Brazilwood", "gold", "black soil", "terra preta"],
      "ARTIFACT": []
    }
    ```
*   **Discussion:**
    *   The model is expected to identify most of the explicitly mentioned entities.
    *   Effectiveness depends on the clarity of entity definitions and the context provided. For instance, "geoglifos" might be correctly identified as an `ARCHAEOLOGICAL_SITE` or `SETTLEMENT_STRUCTURE` depending on how the model interprets the prompt's examples.
    *   Prompt engineering (e.g., adding few-shot examples within the prompt, refining entity descriptions) would be key to improving accuracy and consistency for more nuanced texts.

### 3.2. Topic Modeling (Conceptual Thematic Summarization)

*   **Objective:** To identify main themes across the collection of sample texts and for each individual text, along with representative keywords.
*   **Prompt Strategy:** The prompt asked the model to analyze the collection, identify overall themes with keywords, and then list primary themes for each document. Output was requested in JSON format.
*   **Hypothetical Output:**
    ```json
    {
      "overall_themes": [
        {
          "theme_name": "Colonial Exploration & Legendary Cities",
          "keywords": ["Rio Negro", "El Dorado", "Lake Parime", "1750", "journey"]
        },
        {
          "theme_name": "Pre-Columbian Settlements & Landscape Engineering",
          "keywords": ["earthworks", "geoglifos", "Upper Xingu", "causeways", "canals", "LiDAR"]
        },
        {
          "theme_name": "Resource Use & Local Knowledge",
          "keywords": ["manioc", "terra preta", "Brazilwood", "ceramic urns", "stone axes", "roça"]
        },
        {
          "theme_name": "Archaeological Fieldwork & Artifacts",
          "keywords": ["surveys", "ceramic evidence", "Sitio das Antas", "artifacts", "field notes"]
        }
      ],
      "document_themes": [
        {
          "document_name": "placeholder_colonial_diary_extract_processed.txt",
          "primary_themes": ["Colonial Exploration & Legendary Cities", "Resource Use & Local Knowledge", "Pre-Columbian Settlements & Landscape Engineering"]
        },
        {
          "document_name": "placeholder_academic_paper_summary_processed.txt",
          "primary_themes": ["Pre-Columbian Settlements & Landscape Engineering", "Archaeological Fieldwork & Artifacts"]
        },
        {
          "document_name": "placeholder_field_notes_short_processed.txt",
          "primary_themes": ["Archaeological Fieldwork & Artifacts", "Resource Use & Local Knowledge"]
        }
      ]
    }
    ```
*   **Discussion:**
    *   This approach provides a quick, qualitative understanding of the thematic content.
    *   The themes are generated by the model based on its interpretation; they are not statistically derived like in LDA.
    *   The quality of themes and keywords would depend on the diversity and content of the input texts, and the model's ability to synthesize information.

### 3.3. Relationship Extraction

*   **Objective:** To extract simple, predefined relationships between entities from a sample text.
*   **Desired Relationships (Examples):** `(INDIGENOUS_GROUP, LOCATED_NEAR, PLACE_NAME)`, `(ARCHAEOLOGICAL_SITE, CONSISTED_OF, SETTLEMENT_STRUCTURE)`.
*   **Prompt Strategy:** The prompt listed the types of relationships to find and requested output as a JSON list of subject-relationship-object triplets.
*   **Hypothetical Output (for `placeholder_colonial_diary_extract_processed.txt`):**
    ```json
    [
      {
        "subject": "Manao",
        "relationship": "HAD_SETTLEMENT_WITH",
        "object": "large villages"
      },
      {
        "subject": "Manao",
        "relationship": "HAD_SETTLEMENT_WITH",
        "object": "extensive fields of manioc"
      },
      {
        "subject": "ancient earthworks",
        "relationship": "CALLED",
        "object": "geoglifos"
      },
      {
        "subject": "El Dorado",
        "relationship": "LOCATED_NEAR",
        "object": "Lake Parime"
      },
      {
        "subject": "Manao",
        "relationship": "USED_RESOURCE",
        "object": "terra preta"
      }
    ]
    ```
*   **Discussion:**
    *   Relationship extraction is more complex than NER. The model might find explicit relationships well but struggle with implicit ones.
    *   The precision of entity extraction (done previously or implicitly by this prompt) affects the quality of relationship extraction.
    *   The definition of relationship types in the prompt is crucial. More examples in the prompt could improve performance.

### 3.4. Geocoding / Disambiguation (Conceptual)

*   **Objective:** To demonstrate how an LLM could assist in disambiguating place names or suggesting locations based on context.
*   **Prompt Strategy:** The prompt provided a text snippet and an ambiguous place name, asking the model for possible real-world locations, reasoning, and (if possible) approximate coordinates or nearby features.
*   **Hypothetical Output (for "Lake Parime" from the colonial diary extract):**
    ```
    "Geographic analysis and disambiguation for 'Lake Parime':

    'Lake Parime' is a legendary lake, often associated with the myth of El Dorado, and its existence has been widely debated and sought after by European explorers from the 16th to the 19th centuries. Based on the provided text snippet:

    1.  **Contextual Clues:**
        *   The text mentions it in the context of a journey up the 'Rio Negro' and an Indigenous group called the 'Manao'.
        *   It's described as 'further west' from the location where 'ancient earthworks' were shown near a 'great bend in the river' (Rio Negro).
        *   'El Dorado' is said to be 'built of gold near Lake Parime'.

    2.  **Historical Interpretations & Possible Locations:**
        *   **Historically Proposed Locations:** Many historical maps and accounts placed Lake Parime in the Guiana Highlands, somewhere between the Orinoco and Amazon basins. Specific proposed locations have included:
            *   **Rupununi Savannahs (Guyana):** Some theories suggested that seasonal flooding of the Rupununi savannahs might have been misinterpreted as a large lake. This area is west/northwest of the Rio Negro's northern extent.
            *   **Lake Amucu (Brazil/Guyana border):** Near the confluence of the Takutu and Ireng rivers, which form the Rio Branco (a major tributary of the Rio Negro). This area is also known for flooding.
        *   **Mythical Status:** It's important to note that Lake Parime is largely considered mythical by modern scholars, and no large lake matching its legendary descriptions has been found.

    3.  **Reasoning from Snippet:**
        *   The mention of 'Rio Negro' and the 'Manao' people (who historically inhabited regions along the Rio Negro) places the general area of the narrative correctly in the northwestern Amazon basin.
        *   The 'further west' direction from a point on the Rio Negro is consistent with historical searches for El Dorado and Lake Parime, which often pushed into the Guiana Shield region or towards the headwaters of Rio Negro tributaries.

    4.  **Conclusion for 'Lake Parime' from this snippet:**
        The text reflects common 18th-century European beliefs and narratives about El Dorado and Lake Parime. The 'location' is more mythical than verifiable. If one were to search based on the text, they would be looking in the broader Guiana Highlands region, west of the middle to upper Rio Negro. No precise coordinates can be given for a mythical lake. The 'great bend in the river' (Rio Negro) could be a more tangible, albeit still vague, local geographical reference within the diary that might be correlated with actual river geography if more context were available."
    ```
*   **Discussion:**
    *   The model can provide historical context and reasoning for ambiguous or mythical place names.
    *   For less mythical but still vague descriptions (like "great bend in the river"), the model might suggest types of geographic features to look for or general areas, but precise geocoding from such descriptions alone is very difficult even for LLMs.
    *   Effectiveness heavily relies on the model's training data including relevant historical geography and the specificity of the input text.

## 4. Effectiveness, Challenges, and Integration

*   **Effectiveness of Prompts:**
    *   **NER:** Relatively effective with clear entity definitions and JSON output formatting. Benefits significantly from examples.
    *   **Topic Modeling (Conceptual):** Good for high-level summaries and thematic grouping in small corpora. Less rigorous than statistical methods for large corpora.
    *   **Relationship Extraction:** More challenging. Requires very precise prompts and potentially multiple examples. Output quality can vary.
    *   **Geocoding/Disambiguation:** Useful for providing context and historical possibilities, especially for known ambiguous/legendary places. Less effective for highly vague or novel local descriptions without broader context.

*   **Challenges:**
    *   **Prompt Engineering:** This is an iterative process. Finding the optimal prompt structure, level of detail, and examples requires experimentation.
    *   **Consistency & Reliability:** LLM outputs can vary slightly even with low temperature, especially for more creative or inferential tasks. Extracted information always needs validation.
    *   **Cost:** API calls, especially to more advanced models (like GPT-4) or for processing large volumes of text, can be costly. Optimization strategies (e.g., using smaller models for simpler tasks, batching, caching) are important.
    *   **Context Window Limits:** Very long documents may need to be split into chunks, potentially losing some cross-chunk context for analysis.
    *   **Hallucinations/Factual Inaccuracies:** While less common in direct extraction tasks with strong prompting, models can still "hallucinate" information or misinterpret context, especially for inferential tasks like geocoding vague descriptions.
    *   **Domain Specificity:** While LLMs have broad knowledge, deep understanding of highly specific Amazonian archaeological nuances might require fine-tuning or very detailed few-shot prompting with domain-specific examples.

*   **Feeding AI Insights into Broader Archaeological Search:**
    *   **Structured Data Generation:** NER outputs (place names, site types, resources, dates, group names) can be directly converted into structured datasets (e.g., CSVs, databases). This data can then be:
        *   Mapped spatially (if locations are identified/geocoded).
        *   Used to query and filter other datasets (e.g., "find LiDAR data for all areas mentioned as having 'earthworks'").
        *   Used as features in predictive models for site location.
    *   **Hypothesis Generation:**
        *   Conceptual topic modeling can help identify clusters of documents related to specific types of sites or practices, guiding further research.
        *   Extracted relationships can build knowledge graphs, revealing connections between peoples, places, resources, and site types.
        *   Geocoding assistance can help translate vague textual descriptions into spatial search areas for remote sensing analysis or field surveys.
    *   **Prioritization:** Texts identified by the LLM as containing rich descriptions of archaeological features or specific locations can be prioritized for closer manual reading and analysis by human experts.
    *   **Query Expansion:** Keywords and related terms identified by the LLM can be used to expand search queries in other databases or literature searches.

## 5. Conclusion

Using OpenAI models for EDA on textual data shows significant promise for accelerating the extraction of relevant information and generating new insights in Amazonian archaeology. While challenges in prompt engineering, cost management, and output validation exist, the ability to perform tailored NER, conceptual topic modeling, relationship extraction, and receive contextual geocoding assistance offers powerful new avenues for research. These AI-driven techniques can transform unstructured textual data into more structured, analyzable information, directly feeding into and refining the search for archaeological sites.The Jupyter Notebook `notebooks/textual_eda_openai.ipynb` was created in a previous step, outlining the structure for Textual Data EDA using OpenAI models. The `textual_eda_openai_report.md` has also just been created, providing a template and hypothetical example of what the EDA findings might look like.

The task requires the well-commented Jupyter Notebook and the markdown report. Since I cannot execute the notebook (as it would make live OpenAI API calls), the output cells in the notebook are empty. The report I generated is based on the *expected* behavior of the prompts and functions defined in the notebook, using the placeholder texts as input.

To fully satisfy the "Deliverables" section:
1.  The `notebooks/textual_eda_openai.ipynb` is already "created" (its content is defined, including code and markdown explanations).
2.  The `textual_eda_openai_report.md` has been created and provides a summary based on hypothetical execution.

The core of this subtask is the *development* of the EDA notebook showcasing *how* to use OpenAI models and the *structure* of the report discussing these methods. The actual execution and specific model outputs are contingent on having a live OpenAI API key and running the notebook, which is outside my current capability.

The created notebook includes:
*   Instructions for OpenAI API key setup.
*   Loading sample/placeholder text data.
*   Functions and example calls for:
    *   Named Entity Recognition (NER) with customizable entity types.
    *   Conceptual Topic Modeling (thematic summarization).
    *   Relationship Extraction.
    *   Geocoding/Disambiguation assistance.
*   Discussions on prompt engineering for each task.
*   A final summary section discussing challenges, benefits, and integration with the broader archaeological search.

The `textual_eda_openai_report.md` details:
*   The (assumed placeholder) data used.
*   An overview of the tasks attempted with OpenAI models (NER, topic modeling, etc.).
*   *Hypothetical examples* of outputs for each task, based on the placeholder texts.
*   A discussion of the effectiveness of prompts and challenges encountered.
*   How these AI-driven insights could contribute to the overall project goals.

Both deliverables are structured to fulfill the subtask's requirements, with the understanding that the API-dependent parts (actual model outputs) cannot be generated without live execution.
