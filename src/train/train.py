import os
import json
import numpy as np
import pandas as pd
import psycopg
import joblib

from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.config import DB_URL
from src.features.build_features import make_features

ART_DIR = "artifacts"
MODEL_PATH = os.path.join(ART_DIR, "model_xgb.joblib")
METRICS_PATH = os.path.join(ART_DIR, "metrics_xgb.json")

FEATURES = ["lag_1", "lag_2", "ma_4", "volatility", "return_1"]

def main():
    os.makedirs(ART_DIR, exist_ok=True)

    # 1) DB
    with psycopg.connect(DB_URL) as conn:
        df = pd.read_sql("SELECT * FROM weekly_stock_prices ORDER BY date", conn)

    # 2) Feature engineering
    feat = make_features(df)
    X = feat[FEATURES]
    y = feat["target_next_close"]

    # 3) Hold-out test
    split_idx = int(len(feat) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    # 4) TimeSeries CV 
    tscv = TimeSeriesSplit(n_splits=5)

    base = XGBRegressor(
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
        tree_method="hist",
        device="cuda",
    )

    # 5) Random Search param space
    param_dist = {
        "n_estimators": [200, 400, 700, 1000],
        "max_depth": [3, 4, 5, 6, 8],
        "learning_rate": [0.01, 0.03, 0.05, 0.08, 0.1],
        "subsample": [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
        "min_child_weight": [1, 3, 5, 7], # cover azsa split yapılmaz
        "reg_alpha": [0.0, 0.01, 0.1, 1.0], # lambda gibi daha keskin
        "reg_lambda": [0.5, 1.0, 2.0, 5.0],
    }

    search = RandomizedSearchCV(
        estimator=base,
        param_distributions=param_dist,
        n_iter=25,  
        cv=tscv,
        scoring="neg_mean_absolute_error",  
        random_state=42,
        n_jobs=-1,
        verbose=1,
    )

    search.fit(X_train, y_train)

    best_params = search.best_params_
    best_cv_mae = -float(search.best_score_)  

    print(" Best params:", best_params)
    print(f"Best CV MAE: {best_cv_mae:.2f}")

    best_model = XGBRegressor(
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
        tree_method="hist",
        device="cuda",
        **best_params
        
    )
    best_model.fit(X_train, y_train)

    preds = best_model.predict(X_test)
    test_mae = mean_absolute_error(y_test, preds)
    test_rmse = np.sqrt(mean_squared_error(y_test, preds))

    print(f"Test MAE : {test_mae:.2f}")
    print(f"Test RMSE: {test_rmse:.2f}")

    joblib.dump({"model": best_model, "features": FEATURES, "best_params": best_params}, MODEL_PATH)

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "best_cv_mae": float(best_cv_mae),
                "test_mae": float(test_mae),
                "test_rmse": float(test_rmse),
                "best_params": best_params,
                "n_rows": int(len(feat)),
                "n_train": int(len(X_train)),
                "n_test": int(len(X_test)),
            },
            f,
            indent=2
        )

    print(f"Saved model  -> {MODEL_PATH}")
    print(f"Saved metrics -> {METRICS_PATH}")

if __name__ == "__main__":
    main()
