import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import seaborn as sns
from wordcloud import WordCloud
# Set seaborn style for better visuals
sns.set(style="whitegrid")
class Visualization:
    def load_data(file_path):
        """Load processed reviews data from a CSV file."""
        try:
            df = pd.read_csv(file_path)
            print("Data loaded successfully.")
            return df
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

    def plot_sentiment_trends(df):
        """Plot sentiment trends for the most recent week."""
        try:
            # Ensure 'date' is datetime
            df['date'] = pd.to_datetime(df['date'])

            # Filter for the last 7 days based on the latest date in the dataset to decrease dencity
            max_date = df['date'].max()
            one_week_df = df[df['date'] >= (max_date - pd.Timedelta(days=6))]

            # Group by day and bank, average sentiment
            daily_avg = one_week_df.groupby([one_week_df['date'].dt.date, 'bank_name'])['sentiment_score'].mean().reset_index()
            daily_avg.rename(columns={'date': 'day'}, inplace=True)

            plt.figure(figsize=(10, 5))
            sns.lineplot(data=daily_avg, x='day', y='sentiment_score', hue='bank_name', marker='o')

            plt.title('Sentiment Trends Over the Last 7 Days')
            plt.xlabel('Date')
            plt.ylabel('Average Sentiment Score')

            # Format x-axis to show day only
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

            print("7-day sentiment trends plot created successfully.")
        except Exception as e:
            print(f"Error creating sentiment trends plot: {str(e)}")

    def plot_rating_distributions(df):
        """Plot rating distributions by bank."""
        try:
            plt.figure(figsize=(10, 5))
            sns.countplot(data=df, x='rating', hue='bank_name')
            plt.title('Rating Distributions by Bank')
            plt.xlabel('Rating')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.show()
            print("Rating distributions plot created successfully.")
        except Exception as e:
            print(f"Error creating rating distributions plot: {str(e)}")

    def plot_keyword_cloud(df):
        """Generate a keyword cloud from review texts."""
        try:
            text = ' '.join(df['review_text'])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Keyword Cloud from Reviews')
            plt.tight_layout()
            plt.show()
            print("Keyword cloud plot created successfully.")
        except Exception as e:
            print(f"Error creating keyword cloud: {str(e)}")