import requests
from services.coinmarketcap_service import fetch_price_cmc

def fetch_price_coingecko(ticker):
    """
    Try Coingecko first, fallback to CoinMarketCap.

    Args:
        ticker (str): Coingecko ID or symbol

    Returns:
        float: USD price
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        data = response.json()
        price = data.get(ticker, {}).get("usd", 0)
        if price > 0:
            return price
        else:
            return fetch_price_cmc(ticker)
    except Exception as e:
        print(f"[Coingecko] Error for {ticker}, trying CMC: {e}")
        return fetch_price_cmc(ticker)
