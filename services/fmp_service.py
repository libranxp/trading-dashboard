import requests
import os
from utils.signal_utils import format_stock_signal

FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_quote(ticker):
    url = f"{BASE_URL}/quote/{ticker}?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return data[0] if data else None
    except Exception as e:
        print(f"[FMP] Error fetching quote for {ticker}: {e}")
        return None

def fetch_profile(ticker):
    url = f"{BASE_URL}/profile/{ticker}?apikey={FMP_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return data[0] if data else None
    except Exception as e:
        print(f"[FMP] Error fetching profile for {ticker}: {e}")
        return None

def scan_stocks(tickers):
    signals = []

    for ticker in tickers:
        quote = fetch_quote(ticker)
        profile = fetch_profile(ticker)

        if not quote or not profile:
            continue

        # Example filter: price change > 3%
        change_pct = quote.get("changesPercentage", 0)
        if abs(change_pct) >= 3:
            signal = format_stock_signal(ticker, quote, profile)
            signals.append(signal)

    return signals
