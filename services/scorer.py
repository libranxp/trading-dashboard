def compute_score(signal):
    score = 0
    if signal.get("spike_detected"):
        score += 5
    if signal.get("volume", 0) > 1_000_000:
        score += 2
    if signal.get("price", 0) > 100:
        score += 1
    if signal.get("source") == "CoinMarketCap":
        score += 1  # Confidence bump for verified source
    return score
