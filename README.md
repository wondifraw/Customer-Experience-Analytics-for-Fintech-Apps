# Customer Experience Analytics for Fintech Apps

This project analyzes user reviews from Ethiopian banking apps on the Google Play Store to gain insights into customer experience and satisfaction. It provides tools for scraping, preprocessing, and analyzing app reviews to help understand user feedback and identify areas for improvement.

## Features

- **Automated Review Scraping**: Fetches reviews from Google Play Store for multiple banking apps
- **Data Preprocessing**: Cleans and standardizes review data
- **Analysis Tools**: Provides insights into:
  - Rating distributions
  - Review sentiment
  - User engagement metrics
  - Temporal trends
- **Interactive Analysis**: Jupyter notebooks for detailed exploration and visualization

## Project Structure

```
Customer-Experience-Analytics-for-Fintech-Apps/
├── data/
│   ├── raw/          # Raw scraped reviews
│   └── processed/    # Cleaned and processed reviews
├── notebooks/
│   ├── banking_app_reviews_analysis.ipynb    # Initial analysis notebook
│   └── google_play_store_analysis.ipynb      # Comprehensive analysis notebook
├── src/
│   ├── playstore_scraper.py     # Review scraping module
│   └── review_preprocessor.py   # Data preprocessing module
├── requirements.txt             # Project dependencies
└── README.md                   # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Jupyter Notebook or JupyterLab (for interactive analysis)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Customer-Experience-Analytics-for-Fintech-Apps.git
   cd Customer-Experience-Analytics-for-Fintech-Apps
   ```

2. Create a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Scraping Reviews

To scrape reviews from Google Play Store:

```python
from src.playstore_scraper import PlayStoreScraper

# Initialize the scraper
scraper = PlayStoreScraper()

# Scrape reviews for all banks
reviews_by_bank = scraper.scrape_all()
```

### 2. Preprocessing Reviews

To preprocess the scraped reviews:

```python
from src.review_preprocessor import ReviewPreprocessor

# Initialize the preprocessor
preprocessor = ReviewPreprocessor()

# Process all reviews
preprocessor.process_all_banks()
```

### 3. Analysis

For detailed analysis, use the provided Jupyter notebooks:

1. Open Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. Navigate to the `notebooks` directory and open either:
   - `banking_app_reviews_analysis.ipynb` for initial analysis
   - `google_play_store_analysis.ipynb` for comprehensive analysis

## Data

The project works with the following banking apps:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

For each app, the following data is collected:
- Review text
- Rating (1-5 stars)
- Date
- Bank name
- Source

## Analysis Features

The analysis notebooks provide:

1. **Basic Statistics**
   - Review counts
   - Average ratings
   - Rating distributions

2. **Review Analysis**
   - Review length analysis
   - Temporal trends
   - User engagement metrics

3. **Visualizations**
   - Rating distributions
   - Monthly review trends
   - Review length distributions
  
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Email: wondebdu@gmail.com