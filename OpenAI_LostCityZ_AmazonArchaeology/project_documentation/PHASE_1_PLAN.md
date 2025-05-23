# Phase 1 Plan: Leveraging Open-Source Data and AI for Amazon Archaeology

## 1. Expand Data Source List

This section details specific, publicly accessible repositories and datasets for each category, prioritizing global sources or those with significant Amazonian coverage.

### Satellite Imagery

*   **Existing:** Landsat, Sentinel
*   **Additional:**
    *   **CBERS (China-Brazil Earth Resources Satellite):** Joint venture providing free imagery, good coverage of South America. ([http://www.cbers.inpe.br/](http://www.cbers.inpe.br/))
    *   **ASTER GDEM (Advanced Spaceborne Thermal Emission and Reflection Radiometer Global Digital Elevation Model):** Provides elevation data, crucial for understanding terrain. ([https://lpdaac.usgs.gov/products/astgtmdemv003/](https://lpdaac.usgs.gov/products/astgtmdemv003/))
    *   **MODIS (Moderate Resolution Imaging Spectroradiometer):** Daily global coverage, useful for land cover and change detection. ([https://modis.gsfc.nasa.gov/data/](https://modis.gsfc.nasa.gov/data/))
    *   **PlanetScope (Planet Labs):** While commercial, they offer research licenses and open data programs for specific initiatives. High-resolution imagery. ([https://www.planet.com/explorer/](https://www.planet.com/explorer/)) (Note: check for open access programs)
    *   **DigitalGlobe Open Data Program:** Provides pre and post-event imagery for disaster relief, which can sometimes include archaeologically relevant areas. ([https://www.digitalglobe.com/ecosystem/open-data](https://www.digitalglobe.com/ecosystem/open-data))

### LiDAR

*   **Existing:** Mentioned as a general category.
*   **Additional:**
    *   **OpenTopography:** A portal for high-resolution topography data, including LiDAR. Coverage is growing, and some Amazonian datasets may become available. ([https://opentopography.org/](https://opentopography.org/))
    *   **INPE (Brazilian National Institute for Space Research):** May host or point to LiDAR data collected for environmental monitoring in the Amazon. ([http://www.inpe.br/](http://www.inpe.br/)) (Requires searching their specific portals)
    *   **National Ecological Observatory Network (NEON):** While primarily US-focused, their data processing tools and standards for LiDAR could be relevant. Some South American research projects might deposit data in related repositories.
    *   **Airborne LiDAR datasets from specific research projects:** Often, these are not in a central repository but published with papers or hosted by universities. Searching academic publications is key.

### Historical Maps

*   **Existing:** David Rumsey Map Collection, Library of Congress
*   **Additional:**
    *   **National Library of Brazil (Biblioteca Nacional do Brasil):** Holds a vast collection of historical maps of Brazil, including the Amazon region. ([https://www.bn.gov.br/](https://www.bn.gov.br/)) (Digital collections accessible online)
    *   **National Archives of Colombia, Peru, Ecuador, Bolivia, Venezuela, Guyana, Suriname, French Guiana:** Each country bordering the Amazon will have its own national archive with historical maps.
    *   **Internet Archive - Maps:** A general repository that often includes digitized historical maps from various sources. ([https://archive.org/details/maps](https://archive.org/details/maps))
    *   **Old Maps Online:** A portal that aggregates historical maps from various institutions worldwide. ([https://www.oldmapsonline.org/](https://www.oldmapsonline.org/))
    *   **Gallica (Bibliothèque nationale de France):** Contains historical maps, including some relevant to French Guiana and historical French claims in the Amazon. ([https://gallica.bnf.fr/](https://gallica.bnf.fr/))

### Textual Data

*   **Existing:** Colonial diaries, Indigenous oral histories, academic papers.
*   **Additional:**
    *   **Project Gutenberg:** Digitized books, including historical accounts and travelogues that might mention the Amazon. ([https://www.gutenberg.org/](https://www.gutenberg.org/))
    *   **HathiTrust Digital Library:** Large-scale collaborative repository of digital content from research libraries, including historical texts. ([https://www.hathitrust.org/](https://www.hathitrust.org/))
    *   **Digital Library of the Caribbean (dLOC):** While focused on the Caribbean, it has materials relevant to the Guianas and northern Amazon. ([https://dloc.com/](https://dloc.com/))
    *   **Internet Archive - Texts:** Vast collection of digitized texts, including many historical documents. ([https://archive.org/details/texts](https://archive.org/details/texts))
    *   **Academic Search Engines (JSTOR, Academia.edu, ResearchGate):** For accessing published research papers. Many universities also have open access repositories.
    *   **Repositories of Indigenous Oral Histories:** These are often specific to individual communities or research projects. Collaboration with local Indigenous organizations and researchers is crucial. Examples include:
        *   **Museu do Índio (Brazil):** May have collections or links to oral history projects. ([https://www.museudoindio.gov.br/](https://www.museudoindio.gov.br/))
        *   **Local cultural heritage centers and NGOs:** Often the primary custodians of such knowledge.

### Archaeological Databases

*   **Existing:** Mentioned as a general category.
*   **Additional:**
    *   **National Inventories/Databases:** Each Amazonian country (Brazil, Peru, Colombia, etc.) will have its own national body responsible for cultural heritage, which may maintain archaeological site databases (e.g., IPHAN in Brazil - Instituto do Patrimônio Histórico e Artístico Nacional). Access levels vary.
    *   **The Digital Archaeological Record (tDAR):** A digital repository for archaeological data, though Amazonian content might be limited but growing. ([https://core.tdar.org/](https://core.tdar.org/))
    *   **Ariadne Portal:** European infrastructure for archaeological data, but may link to relevant global datasets or projects. ([https://portal.ariadne-infrastructure.eu/](https://portal.ariadne-infrastructure.eu/))
    *   **University Research Databases:** Many archaeological projects maintain their own databases. Access often requires contacting the principal investigators.
    *   **Global Human Settlement Layer (GHSL):** While not strictly archaeological, it provides data on human settlements that can be used for predictive modeling of archaeological sites. ([https://ghsl.jrc.ec.europa.eu/](https://ghsl.jrc.ec.europa.eu/))

## 2. Data Access and Storage Strategy

### Common Access Methods

*   **Satellite Imagery:**
    *   **APIs:** Landsat, Sentinel (e.g., Copernicus Open Access Hub, USGS EarthExplorer API), Planet (for subscribers/research programs).
    *   **Direct Download:** USGS EarthExplorer, INPE CBERS catalog, NASA Earthdata Search. Often involves selecting tiles/scenes via a web interface.
    *   **Cloud Platform Access:** AWS Open Data, Google Earth Engine provide direct access to analysis-ready data.
*   **LiDAR:**
    *   **Direct Download:** OpenTopography, specific project websites. Data often in LAZ (compressed) or LAS format.
    *   **APIs:** Some platforms like OpenTopography may offer APIs for data access.
    *   **Request-based:** For some datasets, especially those not yet publicly archived, direct contact with data holders is needed.
*   **Historical Maps:**
    *   **Direct Download:** Most library digital collections (Library of Congress, BnF Gallica, National Library of Brazil) offer downloads (JPEG, TIFF, GeoTIFF if georeferenced).
    *   **APIs/IIIF:** Some institutions use IIIF (International Image Interoperability Framework) for accessing images.
    *   **Web Scraping (Ethical Consideration):** Only if terms of service permit and if no other method is available. Care must be taken not to overload servers.
*   **Textual Data:**
    *   **Direct Download:** Project Gutenberg, Internet Archive (TXT, PDF, EPUB).
    *   **APIs:** Some repositories (e.g., HathiTrust, Europeana) offer APIs for metadata and sometimes content.
    *   **Web Scraping:** For academic papers from university repositories or author websites (if permitted). Use with caution and respect `robots.txt`.
    *   **Data Dumps/Bulk Downloads:** Some platforms (e.g., Wikipedia) offer database dumps.
*   **Archaeological Databases:**
    *   **Web Portals with Search/Download:** tDAR, national inventory portals (access levels vary).
    *   **APIs:** Some modern databases might offer API access.
    *   **Direct Contact/Data Sharing Agreements:** Common for sensitive data or data held by specific research projects/institutions.

### Data Storage Strategy

*   **General Principles:**
    *   **Redundancy:** At least two copies of important data (e.g., cloud + local external drive).
    *   **Organization:** Clear, consistent folder structures and naming conventions are critical. Use a master spreadsheet or database to track datasets, sources, processing status, and metadata.
    *   **Metadata:** Preserve all original metadata. Create additional metadata for processing steps.
*   **Storage Options:**
    *   **Cloud Storage:**
        *   **Pros:** Scalability, accessibility, collaboration, backup often managed by provider.
        *   **Cons:** Cost (can be significant for large volumes), data transfer speeds, security/privacy concerns (choose reputable providers with good data governance).
        *   **Options:** AWS S3, Google Cloud Storage, Azure Blob Storage. Consider "cool" or archival tiers for less frequently accessed data to save costs.
    *   **Local Storage:**
        *   **Pros:** Speed of access (once downloaded), no ongoing costs after initial purchase, full control.
        *   **Cons:** Scalability limited by hardware, risk of data loss (hardware failure, disaster) if not backed up properly, harder for collaboration.
        *   **Options:** Network Attached Storage (NAS) for shared access, high-capacity external hard drives.
    *   **Hybrid Approach:** Use cloud for primary storage and active collaboration, local storage for working copies and backups.
*   **File Formats and Management:**
    *   **Satellite Imagery:**
        *   **Common:** GeoTIFF (raster), NetCDF (multidimensional data), vendor-specific formats (e.g., Sentinel SAFE).
        *   **Management:** Store raw data. Processed data (e.g., corrected, subsetted, indices calculated) should be stored as new files with clear naming. Use GIS software (QGIS, ArcGIS) or libraries (Rasterio, GDAL) for handling.
    *   **LiDAR:**
        *   **Common:** LAS, LAZ (compressed LAS).
        *   **Management:** Store raw point clouds. Derived products (DEMs, DTMs, CHMs) should be stored as GeoTIFFs. Software like CloudCompare, LASTools, PDAL.
    *   **Historical Maps:**
        *   **Common:** TIFF, JPEG (for scans), GeoTIFF (if georeferenced).
        *   **Management:** Store original scans. Georeferenced versions should be clearly marked. Maintain metadata about map projection, source, and georeferencing accuracy.
    *   **Textual Data:**
        *   **Common:** TXT, PDF, DOCX, XML (e.g., TEI for transcribed texts), JSON (for structured extractions).
        *   **Management:** Convert proprietary formats to plain text or structured formats where possible. Store original and converted versions. Use version control (Git) for transcribed texts or extracted data.
    *   **Archaeological Databases:**
        *   **Common:** CSV, Excel (XLSX), Shapefiles (SHP) for spatial data, GeoPackage (GPKG), PostgreSQL/SQLite databases.
        *   **Management:** Convert to open, non-proprietary formats where possible. Ensure spatial data has defined coordinate reference systems. Database dumps should be regularly backed up.

## 3. OpenAI Model Integration Strategy

### Textual Data

*   **Information Extraction:**
    *   **Models:** o3/o4 mini, GPT-4.1
    *   **Use Cases:**
        *   Extract place names (toponyms), dates, names of individuals/groups, and significant events from colonial diaries, historical accounts, and archaeological reports.
        *   Identify descriptions of landscape, resources, or cultural practices.
    *   **Method:** Fine-tuning on domain-specific texts (if available) or few-shot prompting with clear instructions and examples. Output structured data (e.g., JSON) for easier integration with GIS.
*   **Summarization:**
    *   **Models:** o3/o4 mini, GPT-4.1
    *   **Use Cases:** Summarize academic papers to quickly assess relevance. Condense long historical texts to highlight key information related to archaeological contexts.
    *   **Method:** Prompt engineering to guide the desired level of detail and focus.
*   **Translation:**
    *   **Models:** o3/o4 mini (for common languages), GPT-4.1 (for better nuance and less common languages).
    *   **Use Cases:** Translate historical documents (Spanish, Portuguese, French, Dutch) into English or another common project language. Translate Indigenous terms or concepts if contextually appropriate and validated.
    *   **Method:** Standard translation prompts. *Crucial to have human review for accuracy, especially for nuanced historical or cultural content.*
*   **Geocoding Text Descriptions:**
    *   **Models:** o3/o4 mini, GPT-4.1 (in conjunction with GIS tools).
    *   **Use Cases:** Convert textual descriptions of locations (e.g., "two days walk north from the big rock by the river bend") into potential geographic coordinates or search areas.
    *   **Method:** Extract relative spatial information using LLMs, then use this information to query gazetteers or to define search areas in a GIS. This is probabilistic and requires cross-referencing.
*   **Analyzing Indigenous Oral Histories (High Ethical Sensitivity):**
    *   **Models:** GPT-4.1 (for nuanced understanding, but with extreme caution).
    *   **Use Cases:** Identify potential historical events, migration patterns, ancestral territories, or ecological knowledge embedded in oral traditions. *This should ALWAYS be done in collaboration with and guided by the Indigenous communities themselves.*
    *   **Method:**
        *   Focus on themes, recurring motifs, or connections to known archaeological/environmental data, rather than literal interpretations.
        *   LLMs could help transcribe and organize (with permission) oral histories, making them searchable for specific keywords or concepts agreed upon with the community.
        *   *Never use AI to "validate" or "disprove" oral histories. The goal is respectful engagement and potential hypothesis generation for further, community-approved research.*

### Imagery/LiDAR Data

*   **Interpreting Patterns Identified by Other Tools:**
    *   **Models:** o3/o4 mini, GPT-4.1
    *   **Use Cases:** If specialized GIS/remote sensing tools identify anomalies (e.g., unusual vegetation patterns, subtle earthworks), LLMs could be fed descriptions of these patterns and surrounding environmental context to brainstorm potential archaeological interpretations or suggest features to look for in other datasets.
    *   **Method:** Provide detailed textual descriptions of the visual features, their spatial relationships, and environmental context. Ask the model to generate hypotheses based on known archaeological feature types.
*   **Generating Descriptive Captions/Reports:**
    *   **Models:** o3/o4 mini, GPT-4.1
    *   **Use Cases:** Once features are identified (e.g., by a human or another AI), an LLM could help generate standardized descriptive text for reports or database entries, based on feature characteristics and location.
    *   **Method:** Input structured data about the feature (type, dimensions, location, associated finds) and ask the LLM to write a descriptive paragraph.
*   **Formulating Hypotheses Based on Visual Cues:**
    *   **Models:** o3/o4 mini, GPT-4.1
    *   **Use Cases:** Similar to pattern interpretation, if a human analyst observes subtle visual cues in imagery (e.g., faint linear features, soil discolorations), they can describe these to an LLM to get suggestions for what they might represent archaeologically, or what kind of ground-truthing might be useful.
    *   **Method:** Detailed textual prompts describing the visual evidence.

### Combined Data

*   **Correlating Textual Mentions with Geographical Features:**
    *   **Models:** o3/o4 mini, GPT-4.1 + GIS tools.
    *   **Use Cases:**
        *   Link place names extracted from texts to coordinates on maps or in gazetteers.
        *   If a text describes an ancient settlement near a specific type of river confluence, use an LLM to understand the description and then query GIS data to find matching locations.
        *   Correlate descriptions of resource exploitation (e.g., specific clays for pottery, types of stone for tools) with geological maps and known archaeological site distributions.
    *   **Method:** Use LLMs to extract key descriptive elements from texts. Convert these into search queries for GIS databases or use them to filter potential locations.
*   **Synthesizing Information for Site Prediction/Modeling:**
    *   **Models:** o3/o4 mini, GPT-4.1
    *   **Use Cases:** Combine evidence from historical texts (e.g., "villages were often on high ground near water"), LiDAR (showing terrain and ancient earthworks), and satellite imagery (showing current land use and vegetation that might indicate past human activity) to build a narrative or set of parameters for predictive modeling in GIS.
    *   **Method:** LLMs can help synthesize diverse inputs into a coherent set of rules or weighted factors for a predictive model. For example, "If text mentions 'X', and LiDAR shows 'Y' nearby, and satellite imagery shows 'Z', then likelihood of site is high."
*   **Building Narratives for Interpretive Archaeology:**
    *   **Models:** GPT-4.1
    *   **Use Cases:** Once data is gathered and analyzed, LLMs can help weave together findings from different sources (text, imagery, archaeological data) into a coherent historical or archaeological narrative. This is for hypothesis generation and interpretation, not for generating "facts."
    *   **Method:** Provide the LLM with key findings and ask it to help construct a possible story or explanation that fits the evidence.

### Ethical Considerations and Limitations

*   **Cultural Sensitivity with Indigenous Data:**
    *   **Ownership and Control:** Indigenous communities own their cultural heritage, including oral histories and traditional knowledge. Collaboration, consent, and benefit-sharing are paramount. Data should not be extracted or used without explicit, ongoing permission.
    *   **Misinterpretation:** AI can misinterpret nuances of language, metaphor, and cultural context in oral traditions, leading to harmful oversimplifications or misrepresentations. Human expertise and community review are essential.
    *   **Data Sovereignty:** Indigenous communities should have control over how their data is stored, accessed, and used.
*   **Colonial Bias in Historical Texts:**
    *   Colonial documents often reflect the biases, perspectives, and agendas of the colonizers. AI may inadvertently perpetuate these biases if not critically managed.
    *   Texts may omit or distort Indigenous perspectives.
*   **Accuracy and "Hallucinations":**
    *   LLMs can generate plausible but incorrect information ("hallucinations"). All AI-generated information must be critically evaluated and cross-verified with other evidence.
    *   This is especially critical for geocoding or making definitive statements about the past.
*   **Data Privacy:**
    *   Ensure that any personal data in textual sources or databases is handled according to privacy regulations and ethical guidelines.
*   **Accessibility and Digital Divide:**
    *   Relying heavily on digital data and AI tools can exclude researchers or communities with limited access to technology or training.
*   **Over-Reliance on AI:**
    *   AI should be a tool to assist human experts (archaeologists, historians, Indigenous knowledge holders), not replace them. Critical thinking and domain expertise remain essential.
*   **Intellectual Property:**
    *   Be mindful of copyright for textual and map data. Ensure that AI-generated content based on copyrighted material is used appropriately.
*   **Transparency:**
    *   Document the use of AI models, the data they were trained on (if known), and the prompts used, to ensure transparency in the research process.

This document provides a foundational plan. Each point will require further detailed research and methodology development as the project progresses.
