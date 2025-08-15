import json, os

WATCHLIST_FILE = "watchlist/watchlist.json"

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE, "r") as f:
        return json.load(f)

def save_watchlist(tickers):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(tickers, f)

def add_to_watchlist(ticker):
    tickers = load_watchlist()
    if ticker not in tickers:
        tickers.append(ticker)
        save_watchlist(tickers)

def remove_from_watchlist(ticker):
    tickers = load_watchlist()
    if ticker in tickers:
        tickers.remove(ticker)
        save_watchlist(tickers)

def filter_signals_by_watchlist(signals):
    watchlist = load_watchlist()
    return [s for s in signals if s["ticker"] in watchlist]
