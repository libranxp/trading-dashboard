import requests

def enrich_with_news(signals, api_key=None):
    """
    Enrich each signal with recent news data.

    Args:
        signals (list): List of signal dictionaries with 'ticker' or 'name' keys
        api_key (str, optional): API key for external news provider

    Returns:
        list: Enriched signals with news metadata
    """
    if not signals:
        print("[News] No signals provided for enrichment.")
        return []

    enriched = []
    for signal in signals:
        query = signal.get("name") or signal.get("ticker")
        news_data = fetch_news_for_query(query, api_key)

        signal["news"] = {
            "headline": news_data.get("headline"),
            "sentiment": news_data.get("sentiment"),
            "source": news_data.get("source"),
            "published_at": news_data.get("published_at")
        }
        enriched.append(signal)

    return enriched


def fetch_news_for_query(query, api_key=None):
    """
    Fetch news data for a given query string.

    Args:
        query (str): Search term (e.g. coin name or ticker)
        api_key (str, optional): API key for external news provider

    Returns:
        dict: News metadata (headline, sentiment, source, published_at)
    """
    # Placeholder: Replace with real API integration
    # Example: NewsAPI, GNews, Bing News Search, etc.

    # Example stub response
    return {
        "headline": None,
        "sentiment": None,
        "source": None,
        "published_at": None
    }
