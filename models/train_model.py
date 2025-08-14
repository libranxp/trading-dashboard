import pandas as pd
import xgboost as xgb
import joblib

def train_model():
    df = pd.read_csv("data/training_data.csv")  # Must be real, dynamic data
    X = df.drop(columns=["target"])
    y = df["target"]

    model = xgb.XGBRegressor(n_estimators=100, max_depth=4)
    model.fit(X, y)
    joblib.dump(model, "models/xgb_model.pkl")

if __name__ == "__main__":
    train_model()
