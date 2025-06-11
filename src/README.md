# Source Code Directory

This directory contains the source code for the Play Store Review Analysis project. Below is an overview of the files within the `src` folder.

## Files

- **playstore_scraper.py**: 
  - This script is responsible for scraping reviews from the Google Play Store. It uses web scraping techniques to collect user reviews based on specified app identifiers.
  - ### Key Features:
    - Collects reviews for the 3 bank Ids CBE, BOE and Dashen.
    - Handles pagination to retrieve multiple pages of reviews.
    - Saves the scraped data in a structured format (e.g., CSV, JSON).

- **review_preprocessor.py**: 
  - This script processes and cleans the scraped reviews to prepare them for analysis. It includes functions for text normalization, removing unwanted characters, and filtering out irrelevant data.
  - ### Key Features:
    - Text cleaning and normalization.
    - Tokenization and removal of stop words.
    - Saving preprocessed data for further analysis.

## Getting Started

To get started with the project, clone the repository and navigate to the `src` directory:

```bash
git clone <repository-url>
cd <project-directory>/src