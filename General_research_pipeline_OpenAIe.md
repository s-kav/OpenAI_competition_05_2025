# OpenAI to Z Challenge Solution Pipeline

The OpenAI to Z Challenge is a unique opportunity to use OpenAI's cutting-edge AI models to discover undiscovered archaeological sites in the Amazon region. Using the latest o3/o4 mini and GPT-4.1 models, participants will crunch reams of open-source data to uncover ancient settlements hidden beneath the dense forest canopy.

## Understanding the Challenge and its Requirements

The primary mission of the challenge is to discover undiscovered archaeological sites within the Amazon biome, with a focus on Brazil and the possibility of exploring adjacent areas of Bolivia, Colombia, Ecuador, Guyana, Peru, Suriname, Venezuela, and French Guiana. Final submissions must be submitted by 9pm PST on June 29, 2025[^5][^6].

The top five teams will be selected to present their findings live in front of a panel of experts. The winner will receive $250,000 in cash and API credits, as well as funding to continue research with archaeologists and the opportunity for a field expedition to confirm the findings[^5].

### Competition Checkpoints

The organizers have set several progressive checkpoints:

1. **Initial Familiarization with Data and Tools**
- Download LiDAR or Sentinel-2 imagery
- Use OpenAI models to analyze surface features
- Document model version and dataset ID[^3][^15]
2. **Early Researcher** (reward: \$100 in OpenAI credits)
- Integrate two independent data sources
- Detect at least five potential "anomalies"
- Document all data sources and OpenAI model prompts
- Demonstrate use of the detected information for further research[^3][^15]
3. **New Object Detection**
- Select the best find with supporting evidence
- Algorithmic feature detection
- Search for historical textual evidence via GPT
- Comparison with known archaeological features[^3]
4. **Preparation of the final material**
- Creating a detailed description of the find in the cultural context
- Formulating hypotheses about the functions and age of the object
- Proposing a plan for further research with local partners[^3][^6]

## Solution pipeline

### 1. Preparatory stage

#### 1.1. Setting up the infrastructure

- Creating a Git repository for storing code and results
- Setting up the working environment (Jupyter Notebook or similar)
- Installing the necessary libraries for processing geospatial data:
- GDAL/OGR for working with raster and vector data
- Rasterio for processing raster images
- GeoPandas for working with vector data
- Scikit-image for computer vision algorithms
- Python API for integration with OpenAI models[^5][^14]

#### 1.2. Collection and systematization of data sources

- **Satellite and LiDAR data**:
- OpenTopography LiDAR tiles (high-precision data on the relief under the forest cover)
- Sentinel-2 multispectral images
- GEDI satellite data (global laser altimeter)
- TerraBrasilis polygons (database on deforestation in Brazil)[^3][^6]
- **Historical sources**:
- Colonial diaries and maps
- Oral maps of indigenous peoples of Amazonia
- Archival documentaries
- Scientific publications on the archeology of the region[^5][^6]

### 2. Data processing and analysis

#### 2.1. Data preprocessing

- **LiDAR data processing**:
- Filtering of ground and non-ground points
- Creation of a digital elevation model (DEM)
- Application of visualization algorithms to identify microrelief under forest cover
- Calculation of derivative maps (slope, aspect, surface curvature)[^5][^6]
- **Satellite imagery processing**:
- Atmospheric correction
- Calculation of vegetation indices (NDVI, EVI)
- Creation of composite images to improve visualization
- Application of filters to highlight anthropogenic structures[^5]

#### 2.2. Integrating with OpenAI models

- **Using o3/o4 mini to analyze visual data**:
- Loading processed images into the model
- Generating prompts to identify potential archaeological structures
- Obtaining descriptions of surface features in each image
- Extracting key markers of archaeological objects[^5][^12]
- **Using GPT-4.1 to analyze text data**:
- Extracting geographic indications from historical texts
- Correlating historical descriptions with modern geographic coordinates
- Creating a knowledge base of potential archaeological objects
- Generating hypotheses about the functions and characteristics of detected structures[^5][^12]

### 3. Algorithmic object detection

#### 3.1. Developing detection algorithms

- Implementing the Hough transform to detect geometric structures (lines, circles, rectangles)
- Creation of a segmentation model for identifying anthropogenic objects
- Application of machine learning methods to classify potential archaeological features
- Development of a detection reliability assessment system[^3]

#### 3.2. Cross-validation of detections

- Comparison of results from different data sources (LiDAR, satellite images, historical descriptions)
- Calculation of coordinates of potential objects with an accuracy of up to 50 meters
- Filtering of false positive results
- Prioritization of finds by reliability level and archaeological significance[^3][^5]

### 4. In-depth analysis of promising finds

#### 4.1. Detailed study of the top 5 finds

- Creation of highly detailed maps and 3D models
- Analysis of the relative positions of objects and their relationship to the surrounding landscape
- Comparison with known archaeological sites in the region (e.g. Kuhikugu)
- Formulation of hypotheses on cultural affiliation and chronology[^3][^5]

#### 4.2. Integration with historical sources

- Search for confirmation in colonial diaries and oral traditions
- Using GPT-4.1 to extract relevant fragments of text
- Construction of a chronological model of the historical development of the region
- Evaluation of the cultural and historical significance of potential discoveries[^3][^5][^6]

### 5. Preparation of final materials

#### 5.1. Documenting the process and results

- Creating a reproducible data processing pipeline
- Documenting all sources used with identifiers
- Saving all prompts to OpenAI models and the results obtained
- Ensuring the study can be repeated and the same results obtained (±50 m)[^3][^5]

#### 5.2. Creating presentation materials

- Maps with marked finds and their context
- Visualizations of LiDAR and satellite imagery data
- Comparison materials with known archaeological sites
- A two-page PDF explaining the cultural context, hypotheses, and plan for further research[^3][^6]

#### 5.3. Final Submission

- 200-word abstract summarizing the research
- Git repository URL with source code
- Paper with full description of findings and supporting evidence
- Kaggle submission form[^5][^13][^14]

## Checkpoint Strategy

### Checkpoint 1: Basic Data Development

1. Download one LiDAR tile from OpenTopography or one Sentinel-2 scene
2. Perform basic processing (filtering, DEM creation/visualization)
3. Formulate a simple prompt for o3/o4-mini: "Describe surface features in this image, paying special attention to potential anthropogenic structures"
4. Document the model version and dataset ID[^3][^5]

### Early Explorer Checkpoint

1. Integrate the data GEDI and TerraBrasilis polygons
2. Develop an algorithm to detect potential anomalies:
- Analysis of elevation deviations on DEM
- Detection of geometric patterns using Hough transform
- Detection of anomalies in spectral characteristics of satellite images
3. Identify at least five potential archaeological objects with coordinates (WKT or center + radius)
4. Verify the reproducibility of the algorithm (the same five objects ±50 m)
5. Use the detected data to further refine the search using new prompts to OpenAI models[^3][^5][^6]

### Checkpoint 2: Deep analysis of the best find

1. Select the most promising object from those detected
2. Implement algorithmic detection (segmentation, Hough transform)
3. Use GPT-4.1 to extract mentions in historical texts
4. Compare the find with a known archaeological object by shape, size and context
5. Create a detailed report on the find with visualizations and evidence[^3][^5]

## Conclusion

The presented pipeline covers all stages of participation in the OpenAI to Z Challenge competition – from initial data processing to the final submission. The key success factors will be:

1. Effective integration of various data sources
2. Developing accurate algorithms for detecting archaeological structures
3. Skillful use of OpenAI models for analyzing visual and text data
4. Compelling documentation of the process and results

Following this pipeline, we will not only be able to pass all the checkpoints of the competition, but also potentially make a significant archaeological discovery that will expand our understanding of ancient civilizations of the Amazon[^5][^6].

<div style="text-align: center">⁂</div>

[^1]: rules

[^2]: https://www.semanticscholar.org/paper/f24cb1aee0dd81bd5c0c9ef5d3c5f85c67021f09

[^3]: https://cdn.openai.com/pdf/a9455c3b-c6e1-49cf-a5cc-c40ed07c0b9f/checkpoints-openai-to-z-challenge.pdf

[^4]: http://arxiv.org/pdf/1803.05457v1.pdf

[^5]: https://openai.com/openai-to-z-challenge/

[^6]: https://cdn.openai.com/pdf/a9455c3b-c6e1-49cf-a5cc-c40ed07c0b9f/starter-pack-openai-to-z-challenge.pdf

[^7]: http://arxiv.org/pdf/2410.07095.pdf

[^8]: https://arxiv.org/html/2410.07985

[^9]: http://arxiv.org/pdf/1910.07113.pdf

[^10]: http://arxiv.org/pdf/2405.15123.pdf

[^11]: https://arxiv.org/vc/arxiv/papers/1604/1604.04315v1.pdf

[^12]: https://arxiv.org/pdf/2503.04625.pdf

[^13]: https://www.kaggle.com/competitions/openai-to-z-challenge/

[^14]: https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/578996

[^15]: https://www.kaggle.com/competitions/openai-to-z-challenge/code

[^16]: https://arxiv.org/html/2502.06807v1

[^17]: https://www.kaggle.com/competitions/openai-to-z-challenge/data

[^18]: https://community.openai.com/t/openai-to-z-challenge-discover-lost-amazon-cities/1262049

[^19]: https://www.sdsc.edu/news/2021/PR20210727_OpenTopo.html

[^20]: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10130576/

[^21]: https://www.semanticscholar.org/paper/55db309a39816e3af6132c8cf9e4f6c63f1b2bc3

[^22]: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10551796/

[^23]: https://www.semanticscholar.org/paper/b2d3ad265f0aa11fe221f4321db4588b87e8eadf

[^24]: https://arxiv.org/html/2410.21287v1

[^25]: http://arxiv.org/pdf/2412.00154.pdf

[^26]: https://arxiv.org/pdf/2502.06807.pdf

[^27]: https://arxiv.org/pdf/2409.13773.pdf

[^28]: https://originality.ai/blog/openai-scheduled-tasks

[^29]: https://www.pcmag.com/news/openais-operator-ai-agent-can-automate-web-based-tasks

[^30]: https://arcprize.org/blog/oai-o3-pub-breakthrough

[^31]: https://openai.com/index/introducing-operator/

[^32]: https://www.kaggle.com/jay2333/can-generative-ai-go-any-further

[^33]: https://www.kaggle.com/code/sitammeur/generative-ai-kaggle-report/notebook?scriptVersionId=135859468

[^34]: https://arxiv.org/abs/2402.00653

[^35]: https://www.semanticscholar.org/paper/59f87a2464ab1d3c0376ca30d09c9204c89653dd

[^36]: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10580627/

[^37]: https://www.semanticscholar.org/paper/8f6d8408b391b572f0a04f3805cbdad98c2b6933

[^38]: http://arxiv.org/pdf/2111.08171.pdf

[^39]: http://arxiv.org/pdf/2411.05778.pdf

[^40]: https://www.linkedin.com/posts/sachaghi_sam-altman-says-openais-deep-research-can-activity-7295312253514334208-8bgT

[^41]: https://openai.com/index/better-language-models/

[^42]: https://x.com/openaidevs?lang=en

[^43]: https://digitrendz.blog/topic/research-challenges

[^44]: https://www.tomsguide.com/ai/chatgpt/openai-announces-chatgpt-tasks-for-automating-future-actions-heres-how-to-try-it

[^45]: https://stepwise.pl/2024/05/22/top-5-application-challenges-of-large-language-models-llms/

[^46]: https://fortune.com/2024/10/31/openai-chatgpt-search-engine-google-alphabet-4o-model/

[^47]: https://kinews24.de/openai-to-z-challenge-2025/

[^48]: https://atlas.co/data-sources/open-topography/

[^49]: https://arxiv.org/abs/2501.12948

[^50]: https://arxiv.org/abs/2412.05753

[^51]: https://arxiv.org/abs/2302.07427

[^52]: https://arxiv.org/abs/2206.15331

[^53]: https://www.semanticscholar.org/paper/e6523d63756f329c703de440411408a8e90a2403

[^54]: https://www.semanticscholar.org/paper/1b0378d52d8988ffd5ecfb507e23420985171306

[^55]: https://arxiv.org/pdf/2304.03893.pdf

[^56]: https://arxiv.org/pdf/2304.09406.pdf

[^57]: https://arxiv.org/pdf/2201.06910.pdf

[^58]: http://arxiv.org/pdf/2303.16434.pdf

[^59]: https://arxiv.org/pdf/2306.17582.pdf

[^60]: https://arxiv.org/html/2502.01081

[^61]: https://www.kaggle.com/competitions/openai-to-z-challenge

[^62]: https://openai.com/index/sycophancy-in-gpt-4o/

[^63]: https://openai.com/index/instruction-following/

[^64]: https://opentools.ai/news/openai-unveils-tasks-for-chatgpt-a-new-challenger-to-siri-and-alexa

[^65]: https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/579219

[^66]: https://www.kaggle.com/code/thedrcat/how-to-win-a-kaggle-competition

[^67]: https://www.kaggle.com/ravi20076/discussion

[^68]: https://www.ainews.com/p/openai-launches-250k-openai-to-z-challenge-to-find-lost-amazon-civilizations

[^69]: https://www.semanticscholar.org/paper/21b4777948797377deedf4a9f1f58ad13f6b8b5d

[^70]: https://www.semanticscholar.org/paper/f5a48dc12ab360d35d6479f9507c61379b0de9ed

[^71]: https://www.semanticscholar.org/paper/08e9b3788d7669458ea6a712e413fda03bd31f4b

[^72]: https://www.semanticscholar.org/paper/5ecb82d44b0bf2ba7a9ec2237c9d25ab974f0f77

[^73]: https://arxiv.org/abs/2403.15118

[^74]: http://arxiv.org/pdf/2502.01584.pdf

[^75]: https://arxiv.org/pdf/2212.11126.pdf

[^76]: http://arxiv.org/pdf/2502.13295.pdf

[^77]: https://arxiv.org/pdf/2112.15594.pdf

