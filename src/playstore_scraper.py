from google_play_scraper import Sort, reviews
import pandas as pd
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)   

class PlayStoreScraper:
    def __init__(self):
        """
        Initialize the scraper with target banking apps
        """
        # Dictionary of banking apps with their Play Store IDs
        self.apps = {
            'cbe': 'com.combanketh.mobilebanking',
            'boe': 'com.boa.boaMobileBanking',
            'dashen': 'com.dashen.dashensuperapp'
        }
        
        # Create data directory if it doesn't exist
        # os.makedirs('data/raw', exist_ok=True)
    
    def get_reviews(self, app_id, count=600):
        """
        Fetch reviews for a specific app
        
        Args:
            app_id (str): Play Store app ID
            count (int): Number of reviews to fetch
            
        Returns:
            pd.DataFrame: DataFrame containing reviews
        """
        try:
            # Fetch reviews from Play Store
            result, _ = reviews(
                app_id,
                lang='en',  # English reviews only
                country='us',  # US reviews
                sort=Sort.NEWEST,
                count=count
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(result)
            logging.info(f"Successfully fetched {len(df)} reviews for {app_id}")
            return df
            
        except Exception as e:
            logging.error(f"Error fetching reviews for {app_id}: {str(e)}")
            return pd.DataFrame()

    def scrape_all(self):
        """
        Scrape reviews for all banking apps
        
        Returns:
            dict: Dictionary of DataFrames containing reviews for each bank
        """
        all_reviews = {}
        
        for bank, app_id in self.apps.items():
            try:
                logging.info(f"Scraping reviews for {bank}")
                df = self.get_reviews(app_id)
                
                if not df.empty:
                    # Add bank name and source
                    df['bank'] = bank
                    df['source'] = 'google_play'
                    
                    # Select and rename columns
                    df = df[['content', 'score', 'at', 'bank', 'source']]
                    df.columns = ['review', 'rating', 'date', 'bank', 'source']
                    
                    # Convert timestamp to YYYY-MM-DD
                    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
                    
                    # Save to CSV with new naming format
                    file_path = f'../data/raw/{bank}_review.csv'
                    df.to_csv(file_path, index=False)
                    logging.info(f"Saved {len(df)} reviews for {bank} to {file_path}")
                    
                    all_reviews[bank] = df
                    
            except Exception as e:
                logging.error(f"Error processing {bank}: {str(e)}")
                continue
        
        return all_reviews