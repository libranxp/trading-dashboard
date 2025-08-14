import xgboost as xgb
import numpy as np
import joblib

MODEL_PATH = "models/xgb_model.pkl"

def compute_ai_score(features):
    model = joblib.load(MODEL_PATH)
    input_vector = np.array([features[key] for key in sorted(features.keys())]).reshape(1, -1)
    score = model.predict(input_vector)[0]
    confidence = "High" if score > 8 else "Medium" if score > 7 else "Low"

    narrative = []
    if features.get("rsi") > 70: narrative.append("RSI breakout")
    if features.get("volume") > 1_000_000: narrative.append("whale volume")
    if features.get("sentiment") == 1: narrative.append("bullish sentiment")

    return {
        "ai_score": round(score, 2),
        "confidence": confidence,
        "narrative": " + ".join(narrative),
        "model_used": "XGBoost"
    }
