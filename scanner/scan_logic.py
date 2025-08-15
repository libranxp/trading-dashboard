import os
from dotenv import load_dotenv
from datetime import datetime

import requests
from services.polygon_api import fetch_active_tickers, analyze_ticker
from services.fmp_service import enrich_with_fmp
from services.coinmarketcap_service import fetch_top_crypto_metrics
from services.news_service import enrich_with_news
from services.twitter_service import enrich_with_twitter
from services.reddit_service import enrich_with_reddit
from utils.signal_utils import format_crypto_signal
from watchlist.watchlist_manager import auto_add_to_watchlist, auto_clean_watchlist

load_dotenv()

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
        signal.update({
            "type": "stock",
            "time": datetime.now().strftime("%H:%M"),
            "source": "scanner"
        })

    return enriched

def scan_crypto():
    raw_metrics = fetch_top_crypto_metrics(limit=50)

    raw_signals = [
        format_crypto_signal(m["ticker"], m)
        for m in raw_metrics
    ]

    if not raw_signals:
        return []

    enriched = enrich_with_news(raw_signals)
    enriched = enrich_with_twitter(enriched)
    enriched = enrich_with_reddit(enriched)

    for signal in enriched:
        signal.update({
            "type": "crypto",
            "time": datetime.now().strftime("%H:%M"),
            "source": "scanner"
        })

    return enriched

def run_scan():
    print("[Scan] Starting full scan...")
    stock_signals = scan_stocks()
    crypto_signals = scan_crypto()
    all_signals = stock_signals + crypto_signals

    auto_add_to_watchlist(all_signals)
    auto_clean_watchlist()

    print(f"[Scan] Completed. Total signals: {len(all_signals)}")
    return all_signals
