import requests, time, os

def fetch_crypto_signals():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")}
    params = {"limit": 50, "convert": "USD"}

    response = requests.get(url, headers=headers, params=params)
    data = response.json().get("data", [])

    signals = []
    for asset in data:
        signals.append({
            "ticker": asset["symbol"],
            "score": round(asset["quote"]["USD"]["percent_change_24h"], 2),
            "sentiment": None,
            "volume": asset["quote"]["USD"]["volume_24h"],
            "catalyst": None,
            "time": time.strftime("%H:%M"),
            "type": "crypto"
        })
    return signals
