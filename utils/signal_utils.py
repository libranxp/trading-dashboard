from datetime import datetime

def format_stock_signal(ticker, quote, profile):
    return {
        "ticker": ticker,
        "price": round(quote.get("price", 0), 2),
        "change": round(quote.get("changesPercentage", 0), 2),
        "score": 8.5,  # You can replace this with dynamic scoring later
        "type": "stock",
        "company": profile.get("companyName", "Unknown"),
        "sector": profile.get("sector", "Unknown"),
        "chart_url": f"https://www.tradingview.com/symbols/{ticker}/",
        "timestamp": datetime.now().strftime("%H:%M BST")
    }

def format_crypto_signal(ticker, metrics):
    return {
        "ticker": ticker.upper(),
        "price": round(metrics.get("price", 0), 4),
        "change": round(metrics.get("price_change", 0), 2),
        "score": 8.2,  # You can replace this with dynamic scoring later
        "type": "crypto",
        "market_cap": metrics.get("market_cap", 0),
        "volume": metrics.get("volume", 0),
        "chart_url": f"https://www.tradingview.com/symbols/{ticker.upper()}USD/",
        "timestamp": datetime.now().strftime("%H:%M BST")
    }
