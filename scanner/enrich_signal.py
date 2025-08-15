from services.news_service import enrich_with_news
from services.twitter_service import enrich_with_twitter
from services.reddit_service import enrich_with_reddit
from services.polygon_service import enrich_with_polygon
from services.coingecko_service import enrich_with_coingecko

def enrich_signals(signals):
    signals = enrich_with_news(signals)
    signals = enrich_with_twitter(signals)
    signals = enrich_with_reddit(signals)
    signals = enrich_with_polygon(signals)
    signals = enrich_with_coingecko(signals)
    return signals
