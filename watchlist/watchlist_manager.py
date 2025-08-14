import json
import os
from datetime import datetime, timedelta

WATCHLIST_PATH = "watchlist/watchlist.json"

def load_watchlist():
    if not os.path.exists(WATCHLIST_PATH):
        return []
    with open(WATCHLIST_PATH, "r") as f:
        return json.load(f)

def save_watchlist(data):
    with open(WATCHLIST_PATH, "w") as f:
        json.dump(data, f, indent=2)

def auto_add_to_watchlist(signals):
    watchlist = load_watchlist()
    existing = {item["ticker"]: item for item in watchlist}

    for signal in signals:
        score = signal.get("score", 0)
        sentiment = signal.get("sentiment", "").lower()
        catalyst = signal.get("catalyst", "")
        volume = signal.get("volume", 0)

        if score >= 7 or "bullish" in sentiment or catalyst or volume > 1_000_000:
            item = {
                "ticker": signal["ticker"],
                "type": signal["type"],
                "added_by": signal.get("source", "scanner"),
                "ai_score": score,
                "sentiment": sentiment,
                "last_scan": datetime.utcnow().isoformat()
            }
            existing[signal["ticker"]] = item

    save_watchlist(list(existing.values()))

def auto_clean_watchlist():
    watchlist = load_watchlist()
    cleaned = []

    for item in watchlist:
        score = item.get("ai_score", 0)
        sentiment = item.get("sentiment", "")
        last_scan = datetime.fromisoformat(item.get("last_scan", datetime.utcnow().isoformat()))
        age = datetime.utcnow() - last_scan

        if score < 5 or "bearish" in sentiment or age > timedelta(hours=48):
            continue
        cleaned.append(item)

    save_watchlist(cleaned)
