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
    
    def load_data(self):
        """
        Load all processed review data and return a combined DataFrame
        
        Returns:
            pd.DataFrame: Combined DataFrame with all processed reviews
        """
        try:
            # Find all processed review files
            processed_files = glob.glob('../data/processed/*_review.csv')
            if not processed_files:
                logging.error("No processed review files found")
                return pd.DataFrame()
            
            # Read and combine all files
            dfs = []
            for file in processed_files:
                try:
                    df = pd.read_csv(file)
                    # Only rename if the old column names exist
                    if 'review' in df.columns and 'review_text' not in df.columns:
                        df = df.rename(columns={'review': 'review_text'})
                    if 'bank' in df.columns and 'bank_name' not in df.columns:
                        df = df.rename(columns={'bank': 'bank_name'})
                    dfs.append(df)
                except Exception as e:
                    logging.error(f"Error reading file {file}: {str(e)}")
                    continue
            
            if not dfs:
                logging.error("No data could be loaded from any file")
                return pd.DataFrame()
            
            # Combine all DataFrames
            combined_df = pd.concat(dfs, ignore_index=True)
            return combined_df
            
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()
    
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
            
            processed_df = df.copy()
            
            # Ensure we have the correct column names
            if 'review' in processed_df.columns:
                processed_df = processed_df.rename(columns={'review': 'review_text'})
            if 'bank' in processed_df.columns:
                processed_df = processed_df.rename(columns={'bank': 'bank_name'})
                
            # Clean review text
            processed_df['review_text'] = processed_df['review_text'].apply(self.clean_review)
            
            # Remove empty reviews
            processed_df = processed_df[processed_df['review_text'].str.len() > 0]
            
            # Remove duplicates
            processed_df = processed_df.drop_duplicates(subset=['review_text', 'bank_name'])
            
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

