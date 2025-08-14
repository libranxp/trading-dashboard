import os
import requests

def send_telegram_alert(message, asset_type):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID_CRYPTO") if asset_type == "crypto" else os.getenv("TELEGRAM_CHAT_ID_STOCKS")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"❌ Telegram error: {response.text}")
