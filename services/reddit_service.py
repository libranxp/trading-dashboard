import os
import requests

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")

def fetch_reddit_mentions(ticker):
    try:
        headers = {"User-Agent": "trading-dashboard"}
        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET)
        data = {"grant_type": "client_credentials"}
        token = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers).json()["access_token"]

        headers["Authorization"] = f"bearer {token}"
        url = f"https://oauth.reddit.com/search?q={ticker}&limit=5"
        response = requests.get(url, headers=headers)
        posts = response.json().get("data", {}).get("children", [])
        return [p["data"]["title"] for p in posts]
    except Exception as e:
        print(f"[Reddit] Error fetching mentions for {ticker}: {e}")
        return []
