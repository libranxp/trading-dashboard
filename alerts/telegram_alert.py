import requests, os

def send_telegram_alert(signal):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID_CRYPTO") if signal["type"] == "crypto" else os.getenv("TELEGRAM_CHAT_ID_STOCKS")
    text = f"🚨 {signal['ticker']} triggered!\nScore: {signal['score']}\nVolume: {signal['volume']}\nTime: {signal['time']}\nSentiment: {signal['sentiment']}\nCatalyst: {signal['catalyst']}"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})
