# FARM-SENSE X - Synthetic Dataset Generator

import csv
import os
import random
from mapper import map_inputs
from decision_engine import simple_fusion
from utils import now_date_time


LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs.csv")


OPTIONS = {
    "Soil_feel":["Wet","Normal","Dry","Hard-Dry"],
    "Field_water":["Too much","Normal","Low","Very low"],
    "Insects_seen":["Many","Few","None","Not sure"],
    "Leaf_condition":["Holes / eaten","Spots / color change","Curled leaves","Leaves normal"],
    "Wind_condition":["Strong","Light","No wind"],
    "Weather":["Clear","Cloudy","Light rain","Heavy rain","Not sure"],
    "Crop":["Maize","Wheat","Rice","Cotton","Vegetables","Other"],
    "Crop_stage":["Early","Mid","Late"],
    "Field_size":["Small","Medium","Large"]
}


NUM_ROWS = 200   


def random_input():
    """Generate one random realistic input row."""
    return {k: random.choice(v) for k, v in OPTIONS.items()}


def ensure_log_header():
    header = [
        "date","time","crop","crop_stage","soil","water",
        "insects","leaf","wind","weather","field_size",
        "action","confidence"
    ]
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)


def generate_data():
    ensure_log_header()
    count = 0

    for _ in range(NUM_ROWS):
    
        sample = random_input()

        
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

        with open(LOG_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        count += 1

    print(f"\n✔ Successfully generated {count} synthetic rows!")
    print(f"✔ Saved to: {LOG_PATH}")


if __name__ == "__main__":
    print("\n========== FARM-SENSE X Synthetic Data Generator ==========")
    generate_data()
