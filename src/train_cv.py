import os
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, f1_score
import xgboost as xgb

from config import config
from mapper import map_inputs

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("TRAIN_CV")


def run_cross_validation(log_path: str = config.LOGS_CSV_PATH) -> None:
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Training log file missing: {log_path}")

    df = pd.read_csv(log_path)
    df = df.dropna(subset=["action"]).reset_index(drop=True)

    def to_mapped_row(row: pd.Series) -> Dict[str, Any]:
        inp = {
            "Soil_feel": row.get("soil"),
            "Field_water": row.get("water"),
            "Insects_seen": row.get("insects"),
            "Leaf_condition": row.get("leaf"),
            "Wind_condition": row.get("wind"),
            "Weather": row.get("weather"),
            "Crop_stage": row.get("crop_stage"),
            "Field_size": row.get("field_size")
        }
        return map_inputs(inp)

    mapped_df = pd.DataFrame(list(df.apply(to_mapped_row, axis=1)))

    X = pd.concat([
        mapped_df.reset_index(drop=True),
        pd.get_dummies(df["crop"], prefix="crop")
    ], axis=1)

    le = LabelEncoder()
    y = le.fit_transform(df["action"])

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    f1_scores = []
    fold = 0

    print("\n========== 5-FOLD CROSS VALIDATION ==========\n")

    for train_idx, test_idx in skf.split(X, y):
        fold += 1
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.1,
            eval_metric="mlogloss",
            random_state=42
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        f1 = float(f1_score(y_test, y_pred, average="weighted"))
        f1_scores.append(f1)

        print(f"---- Fold {fold} ----")
        print(f"Fold Weighted F1-Score: {f1:.4f}")
        print(classification_report(y_test, y_pred, target_names=le.classes_))

    print("========== FINAL CROSS-VALIDATION RESULTS ==========")
    print(f"Mean F1 Score : {np.mean(f1_scores):.4f}")
    print(f"Std Deviation : {np.std(f1_scores):.4f}\n")

    os.makedirs(config.MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(config.MODEL_DIR, "model_cv_last.pkl"))
    joblib.dump(le, os.path.join(config.MODEL_DIR, "label_encoder_cv.pkl"))
    joblib.dump(X.columns.tolist(), os.path.join(config.MODEL_DIR, "feature_columns_cv.pkl"))

    logger.info("Cross-validation model artifacts successfully archived.")


if __name__ == "__main__":
    run_cross_validation()
