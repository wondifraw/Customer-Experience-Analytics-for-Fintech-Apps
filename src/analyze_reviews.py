import pandas as pd
import logging
from sentiment_analyzer import SentimentAnalyzer
from theme_analyzer import ThemeAnalyzer
from review_preprocessor import ReviewPreprocessor

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    """Main function to run sentiment and theme analysis"""
    try:
        setup_logging()
        logging.info("Starting review analysis")

        # Load and preprocess data
        preprocessor = ReviewPreprocessor()
        df = preprocessor.load_data()
        df = preprocessor.process_reviews(df)

        # Sentiment Analysis
        sentiment_analyzer = SentimentAnalyzer()
        df, agg_sentiment = sentiment_analyzer.analyze_reviews(df)
        logging.info("Sentiment analysis completed")

        # Theme Analysis
        theme_analyzer = ThemeAnalyzer()
        themes_by_bank = theme_analyzer.identify_themes(df)
        logging.info("Theme analysis completed")

        # Save results
        output_path = 'data/analyzed_reviews.csv'
        try:
            logging.info(f"Attempting to save results to {output_path}")
            df.to_csv(output_path, index=False)
            logging.info(f"Results saved to {output_path}")
        except Exception as e:
            logging.error(f"Error saving results to {output_path}: {str(e)}")
            # Try to save to a different location
            backup_path = 'analyzed_reviews_backup.csv'
            logging.info(f"Attempting to save results to backup location: {backup_path}")
            df.to_csv(backup_path, index=False)
            logging.info(f"Results saved to backup location: {backup_path}")

        # Print summary
        print("\nSentiment Analysis Summary:")
        print(agg_sentiment)
        print("\nTheme Analysis Summary:")
        for bank, themes in themes_by_bank.items():
            print(f"\n{bank}:")
            for theme, keywords in themes.items():
                print(f"  {theme}: {', '.join(keywords[:5])}")

    except Exception as e:
        logging.error(f"Error in main analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 