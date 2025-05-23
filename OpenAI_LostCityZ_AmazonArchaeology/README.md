# Unveiling Traces of the Past: An AI-Driven Archaeological Survey in the Amazon

## About This Project

This repository contains the complete submission for **"Unveiling Traces of the Past: An AI-Driven Archaeological Survey in the Amazon"** project, developed for the **OpenAI "Lost City of Z" Discovery Challenge**.

The primary purpose of this project is to demonstrate a comprehensive, multi-stage workflow for identifying and prioritizing Potential Interest Zones (PIZs) likely to contain archaeological sites within a designated Amazonian Area of Interest (AOI). It leverages open-source geospatial data (LiDAR, Sentinel-2 satellite imagery), historical and academic textual sources, and advanced Artificial Intelligence (AI) methodologies, including Large Language Models (LLMs) from OpenAI.

## Navigation

*   **Detailed Information:** For a full understanding of the project's methodology, findings, and discussion, please refer to the main report:
    *   [`reports/FINAL_REPORT.md`](reports/FINAL_REPORT.md)
*   **Code:**
    *   Python scripts for data acquisition and preprocessing are located in the [`scripts/`](scripts/) directory, organized by data type (satellite, LiDAR, textual).
    *   Jupyter Notebooks for Exploratory Data Analysis (EDA) and PIZ identification/scoring are in the [`notebooks/`](notebooks/) directory.
*   **Configuration:**
    *   The central configuration file for all scripts and notebooks is [`config/config.ini`](config/config.ini). You will need to add your API keys and adjust paths/parameters here.
*   **Data:**
    *   The project is designed to work with data downloaded into the `data/raw/` directory and processed into `data/processed/`. Due to size constraints, actual raw/processed data is not included. Placeholder structures and example files are provided where appropriate. Instructions for data acquisition are detailed in the main report and pipeline-specific READMEs.
*   **Project Documentation:**
    *   All strategy documents, guidelines, and outlines developed throughout the project are available in [`project_documentation/`](project_documentation/).
*   **Reproducibility:**
    *   For instructions on setting up the environment and running the full pipeline, please see the "Reproducibility" section in the [`reports/FINAL_REPORT.md`](reports/FINAL_REPORT.md) and the `environment.yml` / `requirements.txt` files.

## Core Methodology Overview

1.  **Data Acquisition & Preprocessing:** Automated pipelines for Sentinel-2 imagery, LiDAR point clouds, and textual documents.
2.  **Exploratory Data Analysis (EDA):** Identification of anomalies and archaeologically relevant features using computational techniques and AI-assisted textual analysis.
3.  **Potential Interest Zone (PIZ) Identification:** Integration of multi-source evidence to define zones with high archaeological potential.
4.  **Heuristic Scoring & Prioritization:** Ranking PIZs based on the strength and convergence of evidence.
5.  **AI-Assisted Plausibility Assessment:** Conceptual use of OpenAI LLMs to refine hypotheses for top candidate sites.
6.  **Verification Strategies:** Defined procedures for verifying PIZs using independent methods.

We aim for this project to showcase a reproducible and innovative approach to archaeological remote sensing in challenging environments.

---
*This project was developed as part of the OpenAI "Lost City of Z" Discovery Challenge.*
