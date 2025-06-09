import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# APIs y palabras clave
TWITTER_API = "https://api.twitter.com/2/tweets/search/recent"
NEWS_API = "https://newsapi.org/v2/everything"
KEYWORDS = ["EURUSD", "forex trading", "central bank", "inflation", "market trend"]

analyzer = SentimentIntensityAnalyzer()

def fetch_twitter_sentiment():
    """ Obtiene tweets recientes sobre Forex y analiza el sentimiento """
    headers = {"Authorization": "Bearer YOUR_TWITTER_API_KEY"}
    response = requests.get(TWITTER_API, params={"query": " OR ".join(KEYWORDS)}, headers=headers)

    if response.status_code != 200:
        return pd.DataFrame()

    tweets = response.json()["data"]
    sentiments = [{"text": tweet["text"], "score": analyzer.polarity_scores(tweet["text"])["compound"]} for tweet in tweets]
    return pd.DataFrame(sentiments)

def fetch_news_sentiment():
    """ Analiza el sentimiento de noticias económicas relevantes """
    response = requests.get(NEWS_API, params={"q": " OR ".join(KEYWORDS), "apiKey": "YOUR_NEWS_API_KEY"})

    if response.status_code != 200:
        return pd.DataFrame()

    articles = response.json()["articles"]
    sentiments = [{"title": article["title"], "score": analyzer.polarity_scores(article["title"])["compound"]} for article in articles]
    return pd.DataFrame(sentiments)

if __name__ == "__main__":
    twitter_sentiment = fetch_twitter_sentiment()
    news_sentiment = fetch_news_sentiment()
    print("Twitter Sentiment:\n", twitter_sentiment.head())
    print("News Sentiment:\n", news_sentiment.head())