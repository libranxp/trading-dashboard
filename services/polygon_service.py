import os
import requests
import time

POLYGON_API_KEY = os.getenv("POLYGON_IO_KEY")
FINNHUB_KEY = os.getenv("FINNHUB_KEY")
ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")

def fetch_active_tickers(limit=50):
    try:
        url = f"https://api.polygon.io/v3/reference/tickers?active=true&limit={limit}&apiKey={POLYGON_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("results", [])
        return [item["ticker"] for item in data if "ticker" in item]
    except Exception as e:
        print(f"[Polygon] Error fetching active tickers: {e}")
        return []

def check_price_spike(ticker):
    try:
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/now/now?apiKey={POLYGON_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("results", [])
        if len(data) < 2:
            return False, 0
        latest = data[-1]["c"]
        previous = data[-2]["c"]
        spike = ((latest - previous) / previous) * 100
        return spike > 50, spike
    except Exception as e:
        print(f"[Polygon] Spike check failed for {ticker}: {e}")
        return False, 0

def get_volume_price_polygon(ticker):
    try:
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("results", [{}])[0]
        return {
            "price": data.get("c", 0),
            "volume": data.get("v", 0)
        }
    except Exception as e:
        print(f"[Polygon] Volume/price failed for {ticker}: {e}")
        return {}

def fallback_finnhub(ticker):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return {
            "price": data.get("c", 0),
            "volume": data.get("v", 0),
            "source": "Finnhub"
        }
    except Exception as e:
        print(f"[Finnhub] Fallback failed for {ticker}: {e}")
        return {}

def fallback_alphavantage(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHAVANTAGE_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json().get("Global Quote", {})
        return {
            "price": float(data.get("05. price", 0)),
            "volume": int(data.get("06. volume", 0)),
            "source": "AlphaVantage"
        }
    except Exception as e:
        print(f"[AlphaVantage] Fallback failed for {ticker}: {e}")
        return {}

def enrich_with_polygon(ticker):
    """
    Enrich a ticker with spike detection, volume, price, and scoring.
    Falls back to Finnhub or AlphaVantage if Polygon fails.

    Args:
        ticker (str): Ticker symbol

    Returns:
        dict: Enriched signal
    """
    try:
        spike_detected, spike_pct = check_price_spike(ticker)
        polygon_data = get_volume_price_polygon(ticker)

        if not polygon_data:
            polygon_data = fallback_finnhub(ticker)
        if not polygon_data:
            polygon_data = fallback_alphavantage(ticker)

        score = 0
        if spike_detected:
            score += 5
        if polygon_data.get("volume", 0) > 1_000_000:
            score += 2
        if polygon_data.get("price", 0) > 100:
            score += 1

        return {
            "ticker": ticker,
            "spike_detected": spike_detected,
            "spike_pct": round(spike_pct, 2),
            "price": polygon_data.get("price", 0),
            "volume": polygon_data.get("volume", 0),
            "score": score,
            "source": polygon_data.get("source", "Polygon")
        }

    except Exception as e:
        print(f"[Enrichment] Failed for {ticker}: {e}")
        return {
            "ticker": ticker,
            "error": str(e),
            "score": 0
        }
