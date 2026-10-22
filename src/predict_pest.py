import os
import json
import logging
import numpy as np
from typing import List, Tuple
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("PREDICT_PEST_KERAS")


class KerasPestPredictor:

    def __init__(
        self,
        model_path: str = os.path.join(config.MODEL_DIR, "pest_model_final.h5"),
        label_path: str = os.path.join(config.MODEL_DIR, "pest_label_map.json")
    ) -> None:
        self.model_path = model_path
        self.label_path = label_path
        self.img_size = (224, 224)

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Keras model missing: {self.model_path}")
        if not os.path.exists(self.label_path):
            raise FileNotFoundError(f"Keras label map missing: {self.label_path}")

        self.model = load_model(self.model_path)
        with open(self.label_path, "r", encoding="utf-8") as f:
            self.label_map = json.load(f)

    def predict(self, img_path: str, top_k: int = 3) -> List[Tuple[str, float]]:
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Input image not found: {img_path}")

        img = image.load_img(img_path, target_size=self.img_size)
        x = image.img_to_array(img) / 255.0
        x = np.expand_dims(x, axis=0)

        probs = self.model.predict(x, verbose=0)[0]
        top_indices = probs.argsort()[::-1][:top_k]

        results = [(self.label_map.get(str(idx), f"Class_{idx}"), float(probs[idx])) for idx in top_indices]
        return results


def predict_image(img_path: str, top_k: int = 3) -> List[Tuple[str, float]]:
    predictor = KerasPestPredictor()
    return predictor.predict(img_path, top_k=top_k)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python predict_pest.py <image_path>")
        sys.exit(1)

    target_img = sys.argv[1]
    top_preds = predict_image(target_img, top_k=5)
    print(f"\nTop Predictions for '{target_img}':")
    for cls, prob in top_preds:
        print(f" - {cls}: {prob * 100:.2f}%")
