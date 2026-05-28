# train_tabular.py
# Trains XGBoost model to predict action from logs.csv (FARM-SENSE X)

import os
import pandas as pd
import numpy as np
from mapper import map_inputs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import xgboost as xgb

# Paths
ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(ROOT, "data", "logs.csv")
MODEL_OUT = os.path.join(ROOT, "models")
MODEL_FILE = os.path.join(MODEL_OUT, "model_action.pkl")
ENCODER_FILE = os.path.join(MODEL_OUT, "label_encoder.pkl")

os.makedirs(MODEL_OUT, exist_ok=True)

# 1) Load logs
df = pd.read_csv(LOG_PATH)
print(f"Loaded {len(df)} rows from {LOG_PATH}")

# 2) Basic cleaning: drop rows with missing action
df = df.dropna(subset=["action"]).reset_index(drop=True)

# 3) Feature construction: re-create numeric mapped features using mapper
# We'll create numeric columns: Soil_feel_num, Field_water_num, Insects_seen_num, Leaf_condition_num, Wind_condition_num, Weather_num, Crop_stage_num, Field_size_num
def to_mapped_row(row):
    inp = {
        "Soil_feel": row.get("soil"),
        "Field_water": row.get("water"),
        "Insects_seen": row.get("insects"),
        "Leaf_condition": row.get("leaf"),
        "Wind_condition": row.get("wind"),
        "Weather": row.get("weather"),
        "Crop_stage": row.get("crop_stage"),
        "Field_size": row.get("field_size"),
    }
    mapped = map_inputs(inp)
    return mapped

mapped_rows = df.apply(lambda r: to_mapped_row(r), axis=1)
# Expand mapped dicts into DataFrame
mapped_df = pd.DataFrame(list(mapped_rows))
# Rename columns for clarity
mapped_df = mapped_df.rename(columns={
    "Soil_feel":"soil_num",
    "Field_water":"field_water_num",
    "Insects_seen":"insects_num",
    "Leaf_condition":"leaf_num",
    "Wind_condition":"wind_num",
    "Weather":"weather_num",
    "Crop_stage":"crop_stage_num",
    "Field_size":"field_size_num"
})

# 4) Combine features
X = pd.concat([mapped_df.reset_index(drop=True),
               pd.get_dummies(df["crop"], prefix="crop")], axis=1)

# 5) Label encode target (action)
le = LabelEncoder()
y = le.fit_transform(df["action"])
print("Action classes:", list(le.classes_))

# 6) Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 7) XGBoost model
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="mlogloss",
    random_state=42
)

print("Training XGBoost...")
model.fit(X_train, y_train)

# 8) Evaluate
y_pred = model.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=le.classes_))
print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# 9) Save model + encoder + feature columns
joblib.dump(model, MODEL_FILE)
joblib.dump(le, ENCODER_FILE)
# Save feature columns order for prediction later
feature_columns = X.columns.tolist()
joblib.dump(feature_columns, os.path.join(MODEL_OUT, "feature_columns.pkl"))

print(f"\nSaved model to {MODEL_FILE}")
print(f"Saved encoder to {ENCODER_FILE}")
print(f"Saved feature list to {os.path.join(MODEL_OUT, 'feature_columns.pkl')}")
