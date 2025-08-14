def validate_signal(signal):
    # Stage 1: Filter Validation
    if signal.get("rsi") < 50 or signal.get("volume") < 100000:
        return False

    # Stage 2: AI Score Validation
    if signal.get("ai_score", 0) < 7 or signal.get("confidence") not in ["High", "Medium"]:
        return False

    # Stage 3: Risk Validation
    if signal.get("risk_ratio", 0) < 1.5 or signal.get("risk_level") == "High":
        return False

    # Stage 4: Historical Backtest (optional)
    # Add logic to compare with past failed setups if needed

    return True
