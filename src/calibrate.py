# FARM-SENSE X - Probability Calibration Script (Isotonic)
# Step 3.1: Train calibrated classifier and evaluate reliability

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from mapper import map_inputs
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(ROOT, "data", "logs.csv")
MODEL_DIR = os.path.join(ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

print("\n========== FARM-SENSE X — Calibration (Isotonic) ==========\n")

# Load data
df = pd.read_csv(LOG_PATH)
df = df.dropna(subset=["action"]).reset_index(drop=True)


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

X = pd.concat(
    [mapped_df.reset_index(drop=True),
     pd.get_dummies(df["crop"], prefix="crop")],
    axis=1
)

# Encode labels
le = LabelEncoder()
y = le.fit_transform(df["action"])

# Train-test split for calibration
X_train, X_cal, y_train, y_cal = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Base model
base_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="mlogloss",
    random_state=42
)

print("Training base model...")
base_model.fit(X_train, y_train)

# Calibrate model
print("Calibrating probabilities...")
cal_model = CalibratedClassifierCV(base_model, cv="prefit", method="isotonic")
cal_model.fit(X_cal, y_cal)


y_prob = cal_model.predict_proba(X_cal)


def multiclass_brier_score(y_true, y_prob):
    n_samples = y_true.shape[0]
    y_true_onehot = np.zeros_like(y_prob)
    y_true_onehot[np.arange(n_samples), y_true] = 1
    return np.mean(np.sum((y_prob - y_true_onehot)**2, axis=1))

brier = multiclass_brier_score(y_cal, y_prob)
print(f"\nMulti-class Brier Score (lower = better): {brier:.4f}")

# Classification report
print("\nClassification Report (Calibrated Model):")
y_pred = cal_model.predict(X_cal)
print(classification_report(y_cal, y_pred, target_names=le.classes_))


from sklearn.calibration import calibration_curve

print("\nGenerating reliability diagram...")

max_probs = y_prob.max(axis=1)
correct = (y_pred == y_cal).astype(int)

prob_true, prob_pred = calibration_curve(correct, max_probs, n_bins=10)

plt.figure(figsize=(6,6))
plt.plot(prob_pred, prob_true, marker="o", label="Calibrated (max prob)")
plt.plot([0,1], [0,1], linestyle="--", label="Perfect Calibration")
plt.xlabel("Predicted Confidence")
plt.ylabel("True Accuracy")
plt.title("Reliability Curve (Multiclass Approx.)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(MODEL_DIR, "calibration_plot.png"))
plt.close()

print("\n✔ Calibration plot saved!")
print("✔ Calibrated model saved!\n")
