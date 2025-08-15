import os
import requests

FMP_KEY = os.getenv("FMP_KEY")

def get_fmp_profile(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data[0] if data else {}
    except Exception as e:
        print(f"[FMP] Error fetching profile for {ticker}: {e}")
        return {}
