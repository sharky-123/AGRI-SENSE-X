# FARM-SENSE X - Input Mapping Module

MAPPING = {
    "Soil_feel": {"Wet":47,"Normal":35,"Dry":22,"Hard-Dry":10},
    "Field_water": {"Too much":1.0,"Normal":0.8,"Low":0.5,"Very low":0.2},
    "Insects_seen": {"Many":20,"Few":7,"None":0,"Not sure":None},
    "Leaf_condition": {"Holes / eaten":0.7,"Spots / color change":0.5,"Curled leaves":0.4,"Leaves normal":0.0},
    "Wind_condition": {"Strong":15,"Light":7,"No wind":1},
    "Weather": {"Clear":0,"Cloudy":0.2,"Light rain":3,"Heavy rain":15,"Not sure":None},
    "Field_size": {"Small":0.2,"Medium":0.7,"Large":2.0},
    "Crop_stage": {"Early":0,"Mid":1,"Late":2}
}

def map_inputs(inputs: dict) -> dict:
    numeric = {}
    for key, val in inputs.items():
        if key in MAPPING:
            numeric[key] = MAPPING[key].get(val, None)
        else:
            numeric[key] = val
    return numeric
