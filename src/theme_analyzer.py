import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

class ThemeAnalyzer:
    def __init__(self):
        """Initialize theme analyzer with spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.vectorizer = TfidfVectorizer(
                max_features=100,
                ngram_range=(1, 2),
                stop_words='english'
            )
            logging.info("Theme analyzer initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize theme analyzer: {str(e)}")
            raise

    def extract_keywords(self, text):
        """Extract keywords from text using spaCy"""
        try:
            doc = self.nlp(text)
            # Extract nouns and important phrases
            keywords = [token.text.lower() for token in doc 
                       if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]
            return ' '.join(keywords)
        except Exception as e:
            logging.error(f"Error extracting keywords: {str(e)}")
            return ""

    def identify_themes(self, df):
        """Identify themes from reviews using TF-IDF"""
        try:
            # Extract keywords from reviews
            df['keywords'] = df['review_text'].apply(self.extract_keywords)
            
            # Get TF-IDF features
            tfidf_matrix = self.vectorizer.fit_transform(df['keywords'])
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Group by bank and get top themes
            themes_by_bank = {}
            for bank in df['bank_name'].unique():
                bank_reviews = df[df['bank_name'] == bank]
                bank_tfidf = tfidf_matrix[bank_reviews.index]
                
                # Get top keywords for this bank
                top_keywords = self._get_top_keywords(bank_tfidf, feature_names)
                themes = self._cluster_into_themes(top_keywords)
                themes_by_bank[bank] = themes
            
            return themes_by_bank
        except Exception as e:
            logging.error(f"Error identifying themes: {str(e)}")
            raise

    def _get_top_keywords(self, tfidf_matrix, feature_names, top_n=20):
        """Get top keywords from TF-IDF matrix"""
        try:
            # Sum TF-IDF scores for each feature
            scores = tfidf_matrix.sum(axis=0).A1
            # Get indices of top scores
            top_indices = scores.argsort()[-top_n:][::-1]
            return [feature_names[i] for i in top_indices]
        except Exception as e:
            logging.error(f"Error getting top keywords: {str(e)}")
            return []

    def _cluster_into_themes(self, keywords):
        """Cluster keywords into themes (simplified version)"""
        # Predefined theme categories
        themes = {
            'Account Access': ['login', 'password', 'account', 'access'],
            'Transaction': ['transfer', 'payment', 'transaction', 'money'],
            'UI/UX': ['interface', 'app', 'screen', 'design'],
            'Support': ['support', 'service', 'help', 'contact'],
            'Performance': ['slow', 'fast', 'crash', 'error']
        }
        
        # Assign keywords to themes
        theme_matches = {}
        for theme, theme_keywords in themes.items():
            matches = [k for k in keywords if any(tk in k for tk in theme_keywords)]
            if matches:
                theme_matches[theme] = matches
        
        return theme_matches 