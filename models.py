import requests

def scan_market():
    tickers = ['bitcoin', 'ethereum', 'solana', 'dogecoin']
    results = []

    for ticker in tickers:
        try:
            url = f'https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies=usd'
            response = requests.get(url, timeout=5)
            data = response.json()
            price = data[ticker]['usd']
            results.append({'symbol': ticker.upper(), 'price': price})
        except Exception as e:
            results.append({'symbol': ticker.upper(), 'error': str(e)})

    return results
