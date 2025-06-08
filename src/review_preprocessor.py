import pandas as pd
import logging
import os
import glob

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('preprocessor.log'),
        logging.StreamHandler()
    ]
)

class ReviewPreprocessor:
    def __init__(self):
        """
        Initialize the preprocessor
        """
    
    def clean_review(self, text):
        """
        Clean and standardize review text
        
        Args:
            text (str): Review text to clean
            
        Returns:
            str: Cleaned review text
        """
        try:
            if not isinstance(text, str):
                return ''
            
            # Remove extra whitespace
            text = ' '.join(text.split())
            # Remove special characters but keep basic punctuation
            text = ''.join(char for char in text if char.isalnum() or char in ' .,!?-')
            return text.strip()
            
        except Exception as e:
            logging.error(f"Error cleaning review text: {str(e)}")
            return ''
    
    def process_reviews(self, df):
        """
        Process a DataFrame of reviews
        
        Args:
            df (pd.DataFrame): Raw reviews DataFrame
            
        Returns:
            pd.DataFrame: Processed reviews DataFrame
        """
        try:
            if df.empty:
                return pd.DataFrame()
            
            # Create a copy to avoid modifying original
            processed_df = df.copy()
            
            # Clean review text
            processed_df['review'] = processed_df['review'].apply(self.clean_review)
            
            # Remove empty reviews
            processed_df = processed_df[processed_df['review'].str.len() > 0]
            
            # Remove duplicates
            processed_df = processed_df.drop_duplicates(subset=['review', 'bank'])
            
            # Ensure date format
            processed_df['date'] = pd.to_datetime(processed_df['date']).dt.strftime('%Y-%m-%d')
            
            return processed_df
            
        except Exception as e:
            logging.error(f"Error processing reviews: {str(e)}")
            return pd.DataFrame()
    
    def process_all_banks(self):
        """
        Process reviews for all banks
        """
        try:
            # Create processed directory if it doesn't exist
            os.makedirs('../data/processed', exist_ok=True)
            
            # Get all raw review files
            raw_files = glob.glob('../data/raw/*_review.csv')
            
            for file_path in raw_files:
                try:
                    # Extract bank name from filename using os.path
                    bank = os.path.basename(file_path).replace('_review.csv', '')
                    
                    # Read raw data
                    df = pd.read_csv(file_path)
                    
                    # Process reviews
                    processed_df = self.process_reviews(df)
                    
                    if not processed_df.empty:
                        # Save processed data with new naming format
                        output_path = os.path.join('../data/processed', f'{bank}_review.csv')
                        processed_df.to_csv(output_path, index=False)
                        logging.info(f"Saved {len(processed_df)} processed reviews for {bank}")
                    
                except Exception as e:
                    logging.error(f"Error processing {file_path}: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in process_all_banks: {str(e)}")

if __name__ == "__main__":
    try:
        # Initialize and run preprocessor
        preprocessor = ReviewPreprocessor()
        preprocessor.process_all_banks()
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}") 