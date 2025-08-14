import requests

def scan_crypto(tickers):
    """
    Fetch market data for a list of CoinGecko tickers.

    Args:
        tickers (list): List of CoinGecko coin IDs (e.g. ['bitcoin', 'ethereum'])

    Returns:
        list: List of dictionaries containing market data for each coin
    """
    if not tickers:
        print("[CoinGecko] No tickers provided.")
        return []

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(tickers),
        "order": "market_cap_desc",
        "per_page": len(tickers),
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        signals = []
        for coin in data:
            signal = {
                "ticker": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "price": coin.get("current_price"),
                "price_change_24h": coin.get("price_change_percentage_24h"),
                "volume": coin.get("total_volume"),
                "market_cap": coin.get("market_cap"),
                "last_updated": coin.get("last_updated")
            }
            signals.append(signal)

        return signals

    except requests.exceptions.RequestException as e:
        print(f"[CoinGecko] Request error: {e}")
        return []
    except Exception as e:
        print(f"[CoinGecko] Unexpected error: {e}")
        return []
