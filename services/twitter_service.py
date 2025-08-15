import os
import requests

TWITTER_KEY = os.getenv("TWITTER_KEY")

def fetch_twitter_sentiment(ticker):
    try:
        url = f"https://api.twitter.com/2/tweets/search/recent?query={ticker}&max_results=10"
        headers = {"Authorization": f"Bearer {TWITTER_KEY}"}
        response = requests.get(url, headers=headers)
        tweets = response.json().get("data", [])
        return [t["text"] for t in tweets]
    except Exception as e:
        print(f"[Twitter] Error fetching tweets for {ticker}: {e}")
        return []
