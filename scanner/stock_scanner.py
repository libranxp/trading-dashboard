from services.polygon_service import fetch_active_tickers, analyze_ticker
from services.fmp_service import enrich_with_fmp
from services.news_service import enrich_with_news
from services.twitter_service import enrich_with_twitter
from services.reddit_service import enrich_with_reddit

def scan_stocks():
    """
    Scan and enrich stock signals from multiple sources.

    Returns:
        list: Fully enriched stock signal dictionaries
    """
    tickers = fetch_active_tickers()
    raw_signals = []

    for ticker in tickers:
        signal = analyze_ticker(ticker)
        if signal:
            raw_signals.append(signal)

    if not raw_signals:
        print("⚠️ No stock signals passed initial filters.")
        return []

    # Enrichment pipeline
    enriched = enrich_with_fmp(raw_signals)
    enriched = enrich_with_news(enriched)
    enriched = enrich_with_twitter(enriched)
    enriched = enrich_with_reddit(enriched)

    for signal in enriched:
        signal["type"] = "stock"

    return enriched
