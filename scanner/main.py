from scanner import scan_crypto, scan_stocks

crypto_watchlist = []  # Populate dynamically
stock_watchlist = []   # Populate dynamically

if __name__ == "__main__":
    scan_crypto(crypto_watchlist)
    scan_stocks(stock_watchlist)
