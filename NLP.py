import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


df = pd.read_csv('dataframe2.csv')

sia = SentimentIntensityAnalyzer()

def list_sentiment(list):
    sentiment_list = []
    for i in range(len(list)):
        sentiment_list.append(sia.polarity_scores(list[i]))
    return(sentiment_list)

df['Title sentiment'] = list_sentiment(df['All titles'])






