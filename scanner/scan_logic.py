import os
from dotenv import load_dotenv
from datetime import datetime
import requests

from services.polygon_service import fetch_active_tickers, analyze_ticker
from services.fmp_service import enrich_with_fmp
from services.coingecko_service import scan_crypto as coingecko_scan
from services.news_service import enrich_with_news
from services.twitter_service import enrich_with_twitter
from services.reddit_service import enrich_with_reddit
from utils.signal_utils import format_crypto_signal

from watchlist.watchlist_manager import auto_add_to_watchlist, auto_clean_watchlist

load_dotenv()

def get_top_crypto_ids(limit=20):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [coin["id"] for coin in data if "id" in coin]
    except Exception as e:
        print(f"Error fetching crypto IDs: {e}")
        return []

def scan_stocks():
    tickers = fetch_active_tickers()
    raw_signals = []

    for ticker in tickers:
        signal = analyze_ticker(ticker)
        if signal:
            raw_signals.append(signal)

    if not raw_signals:
        return []

    enriched = enrich_with_fmp(raw_signals)
    enriched = enrich_with_news(enriched)
    enriched = enrich_with_twitter(enriched)
    enriched = enrich_with_reddit(enriched)

    for signal in enriched:
        signal["type"] = "stock"
        signal["time"] = datetime.now().strftime("%H:%M")
        signal["source"] = "scanner"

    return enriched

def scan_crypto():
    crypto_ids = get_top_crypto_ids()
    raw_metrics = coingecko_scan(crypto_ids)
    raw_signals = [format_crypto_signal(m["ticker"], m) for m in raw_metrics]

    if not raw_signals:
        return []

    enriched = enrich_with_news(raw_signals)
    enriched = enrich_with_twitter(enriched)
    enriched = enrich_with_reddit(enriched)

    for signal in enriched:
        signal["type"] = "crypto"
        signal["time"] = datetime.now().strftime("%H:%M")
        signal["source"] = "scanner"

    return enriched

def run_scan():
    stock_signals = scan_stocks()
    crypto_signals = scan_crypto()
    all_signals = stock_signals + crypto_signals

    auto_add_to_watchlist(all_signals)
    auto_clean_watchlist()

    return all_signals
