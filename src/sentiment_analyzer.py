import pandas as pd
from transformers import pipeline
import logging

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer with DistilBERT model"""
        try:
            self.analyzer = pipeline("sentiment-analysis", 
                                   model="distilbert-base-uncased-finetuned-sst-2-english")
            logging.info("Sentiment analyzer initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize sentiment analyzer: {str(e)}")
            raise

    def analyze_sentiment(self, text):
        """Analyze sentiment of a single text"""
        try:
            result = self.analyzer(text)[0]
            return {
                'label': result['label'],
                'score': result['score']
            }
        except Exception as e:
            logging.error(f"Error analyzing sentiment: {str(e)}")
            return {'label': 'ERROR', 'score': 0.0}

    def analyze_reviews(self, df):
        """Analyze sentiment for all reviews in dataframe"""
        try:
            # Apply sentiment analysis to each review
            sentiments = df['review_text'].apply(self.analyze_sentiment)
            
            # Extract labels and scores
            df['sentiment_label'] = sentiments.apply(lambda x: x['label'])
            df['sentiment_score'] = sentiments.apply(lambda x: x['score'])
            
            # Aggregate by bank and rating
            agg_sentiment = df.groupby(['bank_name', 'rating'])['sentiment_score'].mean()
            
            return df, agg_sentiment
        except Exception as e:
            logging.error(f"Error in batch sentiment analysis: {str(e)}")
            raise 