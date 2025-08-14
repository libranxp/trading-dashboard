from services.coingecko_service import scan_crypto
from services.news_service import enrich_with_news
from services.twitter_service import enrich_with_twitter
from services.reddit_service import enrich_with_reddit
from utils.signal_utils import format_crypto_signal

def scan_crypto():
    """
    Scan and enrich crypto signals from CoinGecko and other sources.

    Returns:
        list: Fully enriched crypto signal dictionaries
    """
    # You can load this from config or DB later
    crypto_ids = ["bitcoin", "ethereum", "solana", "dogecoin"]

    raw_metrics = scan_crypto(crypto_ids)
    raw_signals = [format_crypto_signal(m["ticker"], m) for m in raw_metrics]

    if not raw_signals:
        print("⚠️ No crypto signals found.")
        return []

    enriched = enrich_with_news(raw_signals)
    enriched = enrich_with_twitter(enriched)
    enriched = enrich_with_reddit(enriched)

    for signal in enriched:
        signal["type"] = "crypto"

    return enriched
