import os
import requests

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

def fetch_news(ticker, limit=5):
    try:
        url = f"https://newsapi.org/v2/everything?q={ticker}&pageSize={limit}&apiKey={NEWSAPI_KEY}"
        response = requests.get(url, timeout=10)
        articles = response.json().get("articles", [])
        return [{"title": a["title"], "url": a["url"]} for a in articles]
    except Exception as e:
        print(f"[NewsAPI] Error fetching news for {ticker}: {e}")
        return []
