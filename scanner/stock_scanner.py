import requests, time, os

def fetch_stock_signals():
    url = "https://financialmodelingprep.com/api/v3/stock/list"
    key = os.getenv("FMP_KEY")
    response = requests.get(f"{url}?apikey={key}")
    data = response.json()

    signals = []
    for asset in data[:50]:
        ticker = asset["symbol"]
        volume = asset.get("volume", 0)
        score = round(volume / 1e6, 2)

        signals.append({
            "ticker": ticker,
            "score": score,
            "sentiment": None,
            "volume": volume,
            "catalyst": None,
            "time": time.strftime("%H:%M"),
            "type": "stock"
        })
    return signals
