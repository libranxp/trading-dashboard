from services.scorer import compute_ai_score
from services.risk import calculate_risk
from services.validator import validate_signal

def enrich_signal(signal):
    features = {
        "rsi": signal.get("rsi", 50),
        "volume": signal.get("volume", 0),
        "sentiment": 1 if signal.get("sentiment") == "bullish" else 0
    }

    ai = compute_ai_score(features)
    risk = calculate_risk(
        entry_price=signal["price"],
        atr=signal.get("atr", 100),
        support=signal.get("support"),
        resistance=signal.get("resistance")
    )

    signal.update(ai)
    signal.update(risk)
    signal["valid"] = validate_signal(signal)
    return signal
