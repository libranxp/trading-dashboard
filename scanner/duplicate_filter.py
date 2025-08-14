from datetime import datetime, timedelta

alert_cache = {}

def is_duplicate(ticker: str) -> bool:
    now = datetime.utcnow()
    last_alert = alert_cache.get(ticker)
    if last_alert and (now - last_alert) < timedelta(hours=6):
        return True
    alert_cache[ticker] = now
    return False
