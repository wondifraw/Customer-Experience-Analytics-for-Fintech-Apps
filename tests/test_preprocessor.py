import unittest
from unittest.mock import patch, mock_open
import os
import pandas as pd
from src.review_preprocessor import ReviewPreprocessor

class TestReviewPreprocessor(unittest.TestCase):

    def setUp(self):
        """Set up a preprocessor instance before each test."""
        self.preprocessor = ReviewPreprocessor()

    def test_clean_review_standard(self):
        """Test standard review cleaning."""
        review = "  This is a great app!  "
        cleaned = self.preprocessor.clean_review(review)
        self.assertEqual(cleaned, "This is a great app!")

    def test_clean_review_special_chars(self):
        """Test removal of special characters."""
        review = "Awesome! #loveit"
        cleaned = self.preprocessor.clean_review(review)
        self.assertEqual(cleaned, "Awesome! loveit")

    def test_clean_review_extra_whitespace(self):
        """Test removal of extra whitespace."""
        review = "Too    many   spaces"
        cleaned = self.preprocessor.clean_review(review)
        self.assertEqual(cleaned, "Too many spaces")

    def test_clean_review_no_change(self):
        """Test review that requires no changes."""
        review = "Perfectly fine."
        cleaned = self.preprocessor.clean_review(review)
        self.assertEqual(cleaned, "Perfectly fine.")

    def test_clean_review_non_string(self):
        """Test non-string input."""
        review = 123
        cleaned = self.preprocessor.clean_review(review)
        self.assertEqual(cleaned, "")

    def test_process_reviews_standard(self):
        """Test standard DataFrame processing."""
        data = {
            'review': ["  Great app!  ", "Needs improvement.", "  Great app!  "],
            'bank': ['A', 'B', 'A'],
            'date': ['2023-01-01', '2023-01-02', '2023-01-01']
        }
        df = pd.DataFrame(data)
        processed_df = self.preprocessor.process_reviews(df)
        
        self.assertEqual(len(processed_df), 2)
        self.assertEqual(processed_df.iloc[0]['review'], "Great app!")
        self.assertEqual(processed_df.iloc[1]['review'], "Needs improvement.")

    def test_process_reviews_empty_reviews(self):
        """Test removal of empty reviews."""
        data = {
            'review': ["Good", "", "   "],
            'bank': ['A', 'B', 'C'],
            'date': ['2023-01-01', '2023-01-02', '2023-01-03']
        }
        df = pd.DataFrame(data)
        processed_df = self.preprocessor.process_reviews(df)
        
        self.assertEqual(len(processed_df), 1)
        self.assertEqual(processed_df.iloc[0]['review'], "Good")

    def test_process_reviews_empty_df(self):
        """Test processing of an empty DataFrame."""
        df = pd.DataFrame(columns=['review', 'bank', 'date'])
        processed_df = self.preprocessor.process_reviews(df)
        self.assertTrue(processed_df.empty)

    @patch('os.makedirs')
    @patch('glob.glob')
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_process_all_banks(self, mock_to_csv, mock_read_csv, mock_glob, mock_makedirs):
        """Test processing of all banks with file system mocking."""
        # Mock glob to return a dummy file path
        mock_glob.return_value = ['../data/raw/bankA_review.csv']
        
        # Mock read_csv to return a dummy DataFrame
        dummy_data = {
            'review': ['Good app', 'Bad app'],
            'bank': ['A', 'A'],
            'date': ['2023-01-01', '2023-01-02']
        }
        mock_read_csv.return_value = pd.DataFrame(dummy_data)
        
        # Run the method
        self.preprocessor.process_all_banks()
        
        # Assert that makedirs was called
        mock_makedirs.assert_called_once_with('../data/processed', exist_ok=True)
        
        # Assert that read_csv was called with the correct path
        mock_read_csv.assert_called_once_with('../data/raw/bankA_review.csv')
        
        # Assert that to_csv was called with the correct path
        expected_path = os.path.join('../data/processed', 'bankA_review.csv')
        mock_to_csv.assert_called_once_with(expected_path, index=False)

if __name__ == '__main__':
    unittest.main()