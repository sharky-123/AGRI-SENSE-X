import os
import joblib
import numpy as np
from mapper import map_inputs


ROOT = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(ROOT, "models")
MODEL_FILE = os.path.join(MODEL_DIR, "model_action.pkl")
ENCODER_FILE = os.path.join(MODEL_DIR, "label_encoder.pkl")
FEATURES_FILE = os.path.join(MODEL_DIR, "feature_columns.pkl")


model = joblib.load(MODEL_FILE)
label_encoder = joblib.load(ENCODER_FILE)
feature_columns = joblib.load(FEATURES_FILE)

def ml_predict(inputs, ai_score=None):
    """
    inputs = raw farmer input dict
    ai_score = PyTorch Ensemble se aayi probability (optional)
    """

    # Map categorical to numeric
    mapped = map_inputs(inputs)

    
    leaf_val = ai_score if ai_score is not None else mapped.get("Leaf_condition")


    base = {
        "soil_num": mapped.get("Soil_feel"),
        "field_water_num": mapped.get("Field_water"),
        "insects_num": mapped.get("Insects_seen"),
        "leaf_num": leaf_val, 
        "wind_num": mapped.get("Wind_condition"),
        "weather_num": mapped.get("Weather"),
        "crop_stage_num": mapped.get("Crop_stage"),
        "field_size_num": mapped.get("Field_size"),
    }

    
    crop_one_hot = {c:0 for c in feature_columns if c.startswith("crop_")}
    crop_col = "crop_" + inputs["Crop"]
    if crop_col in crop_one_hot:
        crop_one_hot[crop_col] = 1

    
    row = []
    for col in feature_columns:
        if col in base:
            row.append(base[col])
        elif col in crop_one_hot:
            row.append(crop_one_hot[col])
        else:
            row.append(0)

    X = np.array(row).reshape(1, -1)

    
    y_pred = model.predict(X)[0]
    y_prob = float(model.predict_proba(X)[0].max())

    label = label_encoder.inverse_transform([y_pred])[0]

    return label, y_prob