from typing import Dict, Any

MAPPING: Dict[str, Dict[str, float]] = {
    "Soil_feel": {
        "Wet": 47.0,
        "Normal": 35.0,
        "Dry": 22.0,
        "Hard-Dry": 10.0
    },
    "Field_water": {
        "Too much": 1.0,
        "Normal": 0.8,
        "Low": 0.5,
        "Very low": 0.2
    },
    "Insects_seen": {
        "Many": 20.0,
        "Few": 7.0,
        "None": 0.0,
        "Not sure": 0.0
    },
    "Leaf_condition": {
        "Holes / eaten": 0.7,
        "Spots / color change": 0.5,
        "Curled leaves": 0.4,
        "Leaves normal": 0.0
    },
    "Wind_condition": {
        "Strong": 15.0,
        "Light": 7.0,
        "No wind": 1.0
    },
    "Weather": {
        "Clear": 0.0,
        "Cloudy": 0.2,
        "Light rain": 3.0,
        "Heavy rain": 15.0,
        "Not sure": 0.0
    },
    "Field_size": {
        "Small": 0.2,
        "Medium": 0.7,
        "Large": 2.0
    },
    "Crop_stage": {
        "Early": 0.0,
        "Mid": 1.0,
        "Late": 2.0
    }
}


def map_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    numeric_inputs: Dict[str, Any] = {}
    for key, val in inputs.items():
        if key in MAPPING:
            mapped_val = MAPPING[key].get(val, 0.0 if MAPPING[key].get("Not sure") is not None else None)
            numeric_inputs[key] = mapped_val
        else:
            numeric_inputs[key] = val
    return numeric_inputs
