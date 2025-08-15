def is_valid_signal(signal):
    return (
        signal.get("ticker") and
        isinstance(signal.get("price", 0), (int, float)) and
        signal.get("price", 0) > 0 and
        signal.get("volume", 0) >= 0
    )
