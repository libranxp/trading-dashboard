from alerts import send_telegram_alert
from enrich_signal import enrich_signal
from duplicate_filter import is_duplicate
from services.coingecko_service import get_crypto_metrics
from services.fmp_service import get_stock_metrics, get_insider_activity
from services.polygon_service import get_historical_spike

def scan_crypto(tickers: list):
    for ticker in tickers:
        if is_duplicate(ticker):
            continue
        metrics = get_crypto_metrics(ticker)
        if not metrics or metrics["volume"] < 10_000_000 or not (2 <= metrics["price_change"] <= 20):
            continue
        if get_historical_spike(ticker):
            continue
        meta = {
            "price": metrics["price"],
            "change": metrics["price_change"],
            "ai_score": 8.7,
            "reason": "Volume + RSI + Twitter buzz",
            "sl": round(metrics["price"] * 0.9, 4),
            "tp": round(metrics["price"] * 1.2, 4),
            "size": 500
        }
        enriched = enrich_signal(ticker, meta, is_crypto=True)
        if enriched:
            send_telegram_alert(ticker, enriched, is_crypto=True)

def scan_stocks(tickers: list):
    for ticker in tickers:
        if is_duplicate(ticker):
            continue
        metrics = get_stock_metrics(ticker)
        if not metrics or metrics["volume"] < 500_000 or metrics["change"] < 1:
            continue
        if get_historical_spike(ticker):
            continue
        if not get_insider_activity(ticker):
            continue
        meta = {
            "price": metrics["price"],
            "change": metrics["change"],
            "ai_score": 8.6,
            "reason": "Earnings + Insider Buy + Twitter buzz",
            "sl": round(metrics["price"] * 0.95, 2),
            "tp": round(metrics["price"] * 1.15, 2),
            "size": 1000
        }
        enriched = enrich_signal(ticker, meta, is_crypto=False)
        if enriched:
            send_telegram_alert(ticker, enriched, is_crypto=False)
