import os
import requests
from datetime import datetime

def format_alert(data):
    return f"""
🚨 Signal Alert: ${data['ticker']} ({data['type'].capitalize()})

📈 Price: ${data['price']} ({data['change']}%)
📊 AI Score: {data['ai_score']}/10 ✅ {data['confidence']}
🧠 Reason: \"{data['narrative']}\"
📡 Sentiment: {data['sentiment']}
📰 Catalyst: {data['catalyst']}

📍 Risk Panel:
- Stop Loss: ${data['stop_loss']}
- Take Profit: ${data['take_profit']}
- Position Size: ${data['position_size']}

📅 Time: {data['timestamp']}
🔗 [Chart View]({data['chart_url']})
🔗 [News Source]({data['news_url']})
🔗 [Tweet]({data['tweet_url']})

🧭 Commands:
👉 /add {data['ticker']} – Add to Watchlist
👉 /scan {data['ticker']} – Run Manual Scan
👉 /remove {data['ticker']} – Remove from Watchlist
👉 /watchlist – View Watchlist
"""

def send_telegram_alert(signal):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    crypto_chat_id = os.getenv("TELEGRAM_CHAT_ID_CRYPTO")
    stocks_chat_id = os.getenv("TELEGRAM_CHAT_ID_STOCKS")

    chat_id = crypto_chat_id if signal.get("type") == "crypto" else stocks_chat_id
    message = format_alert({
        "ticker": signal["ticker"],
        "type": signal["type"],
        "price": signal["price"],
        "change": signal.get("change_pct", "0.0"),
        "ai_score": signal["ai_score"],
        "confidence": signal["confidence"],
        "narrative": signal["narrative"],
        "sentiment": signal.get("sentiment", "Neutral"),
        "catalyst": signal.get("catalyst", "—"),
        "stop_loss": signal["stop_loss"],
        "take_profit": signal["take_profit"],
        "position_size": signal["position_size"],
        "timestamp": datetime.now().strftime("%H:%M %Z"),
        "chart_url": signal.get("chart_url", "https://tradingview.com"),
        "news_url": signal.get("news_url", "https://newsapi.org"),
        "tweet_url": signal.get("tweet_url", "https://twitter.com")
    })

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    )
