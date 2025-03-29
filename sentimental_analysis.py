import pandas as pd
from transformers import pipeline

# Load the dataset
data = pd.read_csv("output_pdf_data.csv")

# Strip any leading or trailing spaces from the column names
data.columns = data.columns.str.strip()

# Check column names to ensure the correct columns are available
print("Columns in DataFrame:", data.columns)

# Sentiment Analysis using Hugging Face's multilingual model
multilingual_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Function to get the sentiment score for Spanish (or other multilingual) text
def get_multilingual_sentiment_score(text):
    if isinstance(text, str):
        sentiment = multilingual_analyzer(text)
        # 'label' holds the sentiment class, we map it to a numeric score
        sentiment_map = {'1 star': -2, '2 stars': -1, '3 stars': 0, '4 stars': 1, '5 stars': 2}
        return sentiment_map[sentiment[0]['label']]  # Return the sentiment score (numeric)
    else:
        return 0.0  # Neutral score for non-string values

# Apply sentiment analysis to multiple columns, such as Concession Name and Region
data['Concession_Sentiment'] = data['Concession Name'].apply(get_multilingual_sentiment_score)
data['Region_Sentiment'] = data['Region'].apply(get_multilingual_sentiment_score)

# Combine all sentiment scores to get an overall sentiment score (if needed)
data['Overall_Sentiment_Score'] = (data['Concession_Sentiment'] + data['Region_Sentiment']) / 2  # Averaging the sentiment scores

# Save the results
data.to_csv('detailed_analysis_with_sentiments.csv', index=False)

# Display the results
print(data[['Concession Name', 'Concession_Sentiment', 'Region_Sentiment', 'Overall_Sentiment_Score']])
