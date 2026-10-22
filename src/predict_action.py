import os
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, List, Optional
from mapper import map_inputs
from config import config

logger = logging.getLogger(__name__)


class TabularMLPredictor:

    def __init__(
        self,
        model_path: str = config.CALIBRATED_MODEL_PATH,
        encoder_path: str = config.ENCODER_PATH,
        features_path: str = config.FEATURE_COLS_PATH
    ) -> None:
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.features_path = features_path
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Calibrated model file missing: {self.model_path}")
            if not os.path.exists(self.encoder_path):
                raise FileNotFoundError(f"Label encoder file missing: {self.encoder_path}")
            if not os.path.exists(self.features_path):
                raise FileNotFoundError(f"Feature columns artifact missing: {self.features_path}")

            self.model = joblib.load(self.model_path)
            self.encoder = joblib.load(self.encoder_path)
            self.feature_columns: List[str] = joblib.load(self.features_path)

            logger.info("Calibrated ML model, label encoder, and feature column definitions loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML artifacts: {e}", exc_info=True)
            raise RuntimeError(f"ML artifact initialization failed: {e}")

    def predict(self, inputs: Dict[str, Any], ai_score: Optional[float] = None) -> Tuple[str, float]:
        try:
            mapped = map_inputs(inputs)
            df_mapped = pd.DataFrame([mapped])
            df_encoded = pd.get_dummies(df_mapped)

            for col in self.feature_columns:
                if col not in df_encoded:
                    df_encoded[col] = 0

            X_test = df_encoded[self.feature_columns]

            probabilities = self.model.predict_proba(X_test)[0]
            max_idx = int(np.argmax(probabilities))
            max_prob = float(probabilities[max_idx])

            predicted_action = self.encoder.inverse_transform([max_idx])[0]

            logger.info(f"Tabular ML Prediction: '{predicted_action}' (Calibrated Probability: {max_prob:.4f})")
            return predicted_action, max_prob

        except Exception as e:
            logger.error(f"Prediction error during tabular inference: {e}", exc_info=True)
            raise RuntimeError(f"Tabular ML inference failed: {e}")


ml_predictor = TabularMLPredictor()

def ml_predict(inputs: Dict[str, Any], ai_score: Optional[float] = None) -> Tuple[str, float]:
    return ml_predictor.predict(inputs, ai_score)