import os
import joblib
import logging
import pandas as pd
from typing import Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb

from config import config
from mapper import map_inputs

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("TRAIN_TABULAR")


def train_tabular_model(log_path: str = config.LOGS_CSV_PATH) -> None:
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Logs file missing: {log_path}")

    os.makedirs(config.MODEL_DIR, exist_ok=True)

    df = pd.read_csv(log_path)
    df = df.dropna(subset=["action"]).reset_index(drop=True)

    logger.info(f"Loaded {len(df)} samples from log dataset.")

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

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        eval_metric="mlogloss",
        random_state=42
    )

    logger.info("Training XGBoost Classifier...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    print("\n=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    model_file = os.path.join(config.MODEL_DIR, "model_action.pkl")
    encoder_file = os.path.join(config.MODEL_DIR, "label_encoder.pkl")
    features_file = os.path.join(config.MODEL_DIR, "feature_columns.pkl")

    joblib.dump(model, model_file)
    joblib.dump(le, encoder_file)
    joblib.dump(X.columns.tolist(), features_file)

    logger.info(f"Saved tabular model to: {model_file}")
    logger.info(f"Saved label encoder to: {encoder_file}")


if __name__ == "__main__":
    train_tabular_model()
