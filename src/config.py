import os
from dataclasses import dataclass
from typing import Dict

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

@dataclass(frozen=True)
class Config:
    SYSTEM_NAME: str = "FARM-SENSE X"
    SYSTEM_VERSION: str = "2.5"
    ENVIRONMENT: str = os.getenv("APP_ENV", "production")

    ROOT_DIR: str = ROOT_DIR
    SRC_DIR: str = SRC_DIR
    MODEL_DIR: str = os.path.join(ROOT_DIR, "models")
    DATA_DIR: str = os.path.join(ROOT_DIR, "data")
    REPORTS_DIR: str = os.path.join(ROOT_DIR, "reports")
    TEST_IMAGES_DIR: str = os.path.join(ROOT_DIR, "test_images")

    DB_PATH: str = os.path.join(DATA_DIR, "agri_sense.db")
    LOGS_CSV_PATH: str = os.path.join(DATA_DIR, "logs.csv")
    PESTICIDES_CSV_PATH: str = os.path.join(DATA_DIR, "kaggle", "Pesticides.csv")

    ENSEMBLE_MODEL_PATH: str = os.path.join(MODEL_DIR, "ensemble_pest_model.pth")
    CALIBRATED_MODEL_PATH: str = os.path.join(MODEL_DIR, "model_calibrated.pkl")
    ENCODER_PATH: str = os.path.join(MODEL_DIR, "label_encoder_calibrated.pkl")
    FEATURE_COLS_PATH: str = os.path.join(MODEL_DIR, "feature_columns_cv.pkl")
    CALIBRATION_PLOT_PATH: str = os.path.join(MODEL_DIR, "calibration_plot.png")

    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    WEATHER_API_TIMEOUT: int = 5

    RULE_WEIGHT: float = 0.40
    ML_WEIGHT: float = 0.60
    CCI_DECISION_THRESHOLD: float = 0.55
    HIGH_RISK_AI_THRESHOLD: float = 0.80

    PESTICIDE_DB: Dict[str, Dict[str, str]] = None

    @classmethod
    def load_kaggle_pesticides(cls) -> Dict[str, str]:
        pesticide_map: Dict[str, str] = {}
        if os.path.exists(cls.PESTICIDES_CSV_PATH):
            try:
                import csv
                with open(cls.PESTICIDES_CSV_PATH, mode="r", encoding="utf-8-sig") as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    for row in reader:
                        if len(row) >= 2 and row[0].strip():
                            pesticide_map[row[0].strip().lower()] = row[1].strip()
            except Exception:
                pass
        return pesticide_map

    @classmethod
    def get_pesticide_db(cls) -> Dict[str, Dict[str, str]]:
        return {
            "Tomato___Spider_mites Two-spotted_spider_mite": {
                "Chemical": "Abamectin 1.8% EC",
                "Dose": "1 ml/Litre",
                "Organic": "Neem Oil Spray (5 ml/Litre)",
                "Safety": "Wear gloves, avoid eye contact."
            },
            "Tomato___Early_blight": {
                "Chemical": "Mancozeb 75% WP",
                "Dose": "2.5 g/Litre",
                "Organic": "Baking Soda Spray",
                "Safety": "Apply in early morning only."
            },
            "Maize___Common_rust": {
                "Chemical": "Propiconazole 25% EC",
                "Dose": "2 ml/Litre",
                "Organic": "Sulfur Dust",
                "Safety": "Keep cattle away for 48 hours."
            },
            "Maize___Leaf_Blight": {
                "Chemical": "Zineb 75% WP",
                "Dose": "2 g/Litre",
                "Organic": "Garlic-Ginger extract",
                "Safety": "Ensure full leaf coverage."
            },
            "Potato___Late_blight": {
                "Chemical": "Cymoxanil + Mancozeb",
                "Dose": "3 g/Litre",
                "Organic": "Copper-based fungicide",
                "Safety": "Wash hands thoroughly after use."
            },
            "Unknown": {
                "Chemical": "Contact Agricultural Specialist",
                "Dose": "N/A",
                "Organic": "Remove infected leaves manually",
                "Safety": "Do not over-spray chemical treatments."
            }
        }

    @classmethod
    def query_pesticide(cls, query: str) -> Dict[str, str]:
        if not query:
            return cls.get_pesticide_db()["Unknown"]

        base_db = cls.get_pesticide_db()
        if query in base_db:
            return base_db[query]

        q_lower = query.lower().replace("_", " ")
        for key, val in base_db.items():
            if key.lower().replace("_", " ") in q_lower or q_lower in key.lower().replace("_", " "):
                return val

        kaggle_map = cls.load_kaggle_pesticides()
        for pest_name, chemicals in kaggle_map.items():
            p_clean = pest_name.lower().replace("-", " ")
            if p_clean in q_lower or any(word in q_lower for word in p_clean.split() if len(word) > 3):
                return {
                    "Chemical": chemicals,
                    "Dose": "1.5 - 2.0 ml/Litre (Standard dosage)",
                    "Organic": "Cold-pressed Neem Oil Spray (5 ml/Litre)",
                    "Safety": "Target early morning application; wear protective equipment."
                }

        return base_db["Unknown"]

config = Config()
