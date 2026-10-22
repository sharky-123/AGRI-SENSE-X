import csv
import os
import random
import logging
from typing import Dict, List, Any
from config import config
from mapper import map_inputs
from decision_engine import simple_fusion
from utils import now_date_time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("SYNTHETIC_GEN")

FIELD_OPTIONS: Dict[str, List[str]] = {
    "Soil_feel": ["Wet", "Normal", "Dry", "Hard-Dry"],
    "Field_water": ["Too much", "Normal", "Low", "Very low"],
    "Insects_seen": ["Many", "Few", "None", "Not sure"],
    "Leaf_condition": ["Holes / eaten", "Spots / color change", "Curled leaves", "Leaves normal"],
    "Wind_condition": ["Strong", "Light", "No wind"],
    "Weather": ["Clear", "Cloudy", "Light rain", "Heavy rain", "Not sure"],
    "Crop": ["Maize", "Wheat", "Rice", "Cotton", "Vegetables", "Other"],
    "Crop_stage": ["Early", "Mid", "Late"],
    "Field_size": ["Small", "Medium", "Large"]
}


def generate_random_sample() -> Dict[str, str]:
    return {key: random.choice(options) for key, options in FIELD_OPTIONS.items()}


def ensure_csv_header(log_path: str = config.LOGS_CSV_PATH) -> None:
    header = [
        "date", "time", "crop", "crop_stage", "soil", "water",
        "insects", "leaf", "wind", "weather", "field_size",
        "action", "confidence"
    ]
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    if not os.path.exists(log_path):
        with open(log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)


def generate_synthetic_dataset(num_rows: int = 200, log_path: str = config.LOGS_CSV_PATH) -> None:
    ensure_csv_header(log_path)
    count = 0

    for _ in range(num_rows):
        sample = generate_random_sample()
        mapped = map_inputs(sample)
        decision = simple_fusion(mapped)
        date, time = now_date_time()

        row = [
            date, time,
            sample["Crop"], sample["Crop_stage"],
            sample["Soil_feel"], sample["Field_water"],
            sample["Insects_seen"], sample["Leaf_condition"],
            sample["Wind_condition"], sample["Weather"],
            sample["Field_size"],
            decision["action"], decision["confidence"]
        ]

        with open(log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        count += 1

    logger.info(f"Successfully generated {count} synthetic rows saved to: {log_path}")


if __name__ == "__main__":
    logger.info("========== FARM-SENSE X Synthetic Data Generator ==========")
    generate_synthetic_dataset(num_rows=200)
