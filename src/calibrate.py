import os
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    from sklearn.ensemble import HistGradientBoostingClassifier
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from config import config
from mapper import map_inputs

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("CALIBRATE")


def multiclass_brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    n_samples = y_true.shape[0]
    n_classes = y_prob.shape[1]
    y_true_onehot = np.zeros_like(y_prob)
    y_true_onehot[np.arange(n_samples), y_true] = 1.0
    return float(np.mean(np.sum((y_prob - y_true_onehot) ** 2, axis=1)))


def calibrate_and_evaluate(
    log_path: str = config.LOGS_CSV_PATH,
    model_dir: str = config.MODEL_DIR
) -> None:
    logger.info("========== FARM-SENSE X - Calibration (Isotonic) ==========")

    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Training logs file missing at: {log_path}")

    os.makedirs(model_dir, exist_ok=True)

    df = pd.read_csv(log_path)
    df = df.dropna(subset=["action"]).reset_index(drop=True)

    logger.info(f"Loaded {len(df)} training samples from dataset log.")

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

    X_train, X_cal, y_train, y_cal = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    if HAS_XGBOOST:
        base_model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.1,
            eval_metric="mlogloss",
            random_state=42
        )
    else:
        logger.info("XGBoost package not available. Using HistGradientBoostingClassifier fallback.")
        base_model = HistGradientBoostingClassifier(random_state=42)

    logger.info("Fitting Isotonic Calibrated Classifier CV (5-Fold)...")
    cal_model = CalibratedClassifierCV(estimator=base_model, cv=5, method="isotonic")
    cal_model.fit(X_train, y_train)

    y_prob = cal_model.predict_proba(X_cal)
    brier = multiclass_brier_score(y_cal, y_prob)

    logger.info(f"Multi-class Brier Score (lower = better): {brier:.4f}")

    y_pred = cal_model.predict(X_cal)
    print("\nClassification Report (Calibrated Model):")
    print(classification_report(y_cal, y_pred, target_names=le.classes_))

    joblib.dump(cal_model, config.CALIBRATED_MODEL_PATH)
    joblib.dump(le, config.ENCODER_PATH)
    joblib.dump(X.columns.tolist(), config.FEATURE_COLS_PATH)

    logger.info(f"Saved calibrated model to: {config.CALIBRATED_MODEL_PATH}")
    logger.info(f"Saved label encoder to: {config.ENCODER_PATH}")

    if HAS_MATPLOTLIB:
        max_probs = y_prob.max(axis=1)
        correct = (y_pred == y_cal).astype(int)

        prob_true, prob_pred = calibration_curve(correct, max_probs, n_bins=10)

        plt.figure(figsize=(6, 6))
        plt.plot(prob_pred, prob_true, marker="o", label="Calibrated (max prob)")
        plt.plot([0, 1], [0, 1], linestyle="--", label="Perfect Calibration")
        plt.xlabel("Predicted Confidence")
        plt.ylabel("True Accuracy")
        plt.title("Reliability Curve (Isotonic Multiclass)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(config.CALIBRATION_PLOT_PATH)
        plt.close()
        logger.info(f"Calibration plot saved to: {config.CALIBRATION_PLOT_PATH}")
    else:
        logger.warning("Matplotlib not installed. Skipping reliability plot generation.")


if __name__ == "__main__":
    calibrate_and_evaluate()
