# predict_pest.py
# Single-image prediction utility for pest classifier

import os, json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

ROOT = r"C:\agri-sense-x"
MODEL_DIR = os.path.join(ROOT, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "pest_model_final.h5")
LABEL_PATH = os.path.join(MODEL_DIR, "pest_label_map.json")

if not os.path.exists(MODEL_PATH):
    raise SystemExit("Model file not found: " + MODEL_PATH)

model = load_model(MODEL_PATH)
with open(LABEL_PATH, "w") as f:
    label_map = json.load(f)  # index -> class_name

IMG_SIZE = (224, 224)

def predict(img_path, top_k=3):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    probs = model.predict(x)[0]
    idxs = probs.argsort()[::-1][:top_k]
    results = [(label_map[str(i)], float(probs[i])) for i in idxs]
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python predict_pest.py <image_path>")
        sys.exit(1)
    img_path = sys.argv[1]
    print("Predicting:", img_path)
    res = predict(img_path, top_k=5)
    for cls, p in res:
        print(f" - {cls}: {p:.3f}")
