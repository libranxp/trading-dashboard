import os
import requests

CMC_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

def fetch_price_cmc(ticker):
    """
    Fetch price from CoinMarketCap using symbol.

    Args:
        ticker (str): Symbol (e.g., BTC)

    Returns:
        float: USD price
    """
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"symbol": ticker.upper(), "convert": "USD"}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        return data["data"][ticker.upper()]["quote"]["USD"]["price"]
    except Exception as e:
        print(f"[CMC] Error fetching price for {ticker}: {e}")
        return 0
