def assess_risk(signal):
    score = signal.get("score", 0)
    volume = signal.get("volume", 0)
    spike = signal.get("spike_pct", 0)

    if score >= 7 and volume > 1_000_000 and spike > 50:
        return "High"
    elif score >= 4:
        return "Medium"
    else:
        return "Low"
