import os
import requests

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def check_price_spike(ticker):
    """
    Check for abnormal price spike in recent minute.

    Args:
        ticker (str): Ticker symbol

    Returns:
        bool: True if spike > 50%, else False
    """
    try:
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/now/now?apiKey={POLYGON_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json().get("results", [])

        if len(data) < 2:
            return False

        latest = data[-1]["c"]
        previous = data[-2]["c"]
        spike = ((latest - previous) / previous) * 100

        return spike > 50

    except Exception as e:
        print(f"[Polygon] Error checking spike for {ticker}: {e}")
        return False
