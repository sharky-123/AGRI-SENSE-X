# src/train_cv.py

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, f1_score
import xgboost as xgb
from mapper import map_inputs

# Paths
ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(ROOT, "data", "logs.csv")

# Load data
df = pd.read_csv(LOG_PATH)
df = df.dropna(subset=["action"]).reset_index(drop=True)

# Convert each row to numeric mapping
def to_mapped_row(row):
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

mapped_df = pd.DataFrame(list(df.apply(lambda r: to_mapped_row(r), axis=1)))

# Add crop one-hot encoding
X = pd.concat([mapped_df.reset_index(drop=True),
               pd.get_dummies(df["crop"], prefix="crop")],
              axis=1)

# Encode labels
le = LabelEncoder()
y = le.fit_transform(df["action"])

# 5-fold cross-validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
f1s = []
fold = 0

print("\n========== 5-FOLD CROSS VALIDATION ==========\n")

for train_idx, test_idx in skf.split(X, y):
    fold += 1
    print(f"\n---- Fold {fold} ----")

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='mlogloss',
        random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    f1 = f1_score(y_test, y_pred, average='weighted')
    f1s.append(f1)

    print(f"Fold F1 Score: {f1:.3f}")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

print("\n========== FINAL CROSS-VALIDATION RESULTS ==========")
print(f"Mean F1 Score: {np.mean(f1s):.3f}")
print(f"Std deviation: {np.std(f1s):.3f}")

# Save last model + encoder + features
MODEL_DIR = os.path.join(ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, "model_cv_last.pkl"))
joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder_cv.pkl"))
joblib.dump(X.columns.tolist(), os.path.join(MODEL_DIR, "feature_columns_cv.pkl"))

print("\n✔ Saved cross-validation model and artifacts!\n")
