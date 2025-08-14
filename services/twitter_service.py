import os
import requests

TWITTER_BEARER = os.getenv("TWITTER_BEARER_TOKEN")
HEADERS = {"Authorization": f"Bearer {TWITTER_BEARER}"}

def enrich_with_twitter(signals):
    """
    Enrich each signal with Twitter mention summary.

    Args:
        signals (list): List of signal dictionaries with 'ticker' or 'name'

    Returns:
        list: Signals enriched with Twitter summary
    """
    if not signals:
        print("[Twitter] No signals provided.")
        return []

    enriched = []
    for signal in signals:
        query = signal.get("ticker")
        twitter_data = fetch_twitter_summary(query)
        signal["twitter_summary"] = twitter_data
        enriched.append(signal)

    return enriched


def fetch_twitter_summary(query):
    """
    Fetch recent tweet summary for a given ticker.

    Args:
        query (str): Ticker symbol

    Returns:
        str: Summary or placeholder
    """
    try:
        url = f"https://api.twitter.com/2/tweets/search/recent?query=${query}&max_results=10"
        response = requests.get(url, headers=HEADERS, timeout=10)
        tweets = response.json().get("data", [])

        if not tweets:
            return "No recent tweets found."

        top_tweet = tweets[0]
        text = top_tweet.get("text", "No content")
        return f"Top tweet: \"{text[:100]}...\""

    except Exception as e:
        print(f"[Twitter] Error fetching tweets: {e}")
        return "Twitter data unavailable."
