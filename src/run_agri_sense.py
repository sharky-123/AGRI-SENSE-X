import os
import joblib
import numpy as np
import pandas as pd
import sqlite3
import requests
from datetime import datetime
from mapper import map_inputs
from ensemble_predict import AgriEnsemble # Naya Ensemble Import

ROOT = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(ROOT, "models")

# Load calibrated ML model + encoder + feature columns
CAL_MODEL = joblib.load(os.path.join(MODEL_DIR, "model_calibrated.pkl"))
ENCODER = joblib.load(os.path.join(MODEL_DIR, "label_encoder_calibrated.pkl"))
FEATURE_COLS = joblib.load(os.path.join(MODEL_DIR, "feature_columns_cv.pkl"))

PESTICIDE_DB = {
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "Chemical": "Abamectin 1.8% EC", "Dose": "1 ml/Litre",
        "Organic": "Neem Oil Spray (5ml/Litre)", "Safety": "Wear gloves, avoid eye contact."
    },
    "Tomato___Early_blight": {
        "Chemical": "Mancozeb 75% WP", "Dose": "2.5 g/Litre",
        "Organic": "Baking Soda Spray", "Safety": "Apply in early morning only."
    },
    "Maize___Common_rust": {
        "Chemical": "Propiconazole 25% EC", "Dose": "2 ml/Litre",
        "Organic": "Sulfur Dust", "Safety": "Keep cattle away for 48 hours."
    },
    "Maize___Leaf_Blight": {
        "Chemical": "Zineb 75% WP", "Dose": "2 g/Litre",
        "Organic": "Garlic-Ginger extract", "Safety": "Ensure full leaf coverage."
    },
    "Potato___Late_blight": {
        "Chemical": "Cymoxanil + Mancozeb", "Dose": "3 g/Litre",
        "Organic": "Copper-based fungicide", "Safety": "Wash hands thoroughly after use."
    },
    "Unknown": {
        "Chemical": "Contact Agri-Expert", "Dose": "N/A",
        "Organic": "Remove infected leaves manually", "Safety": "Do not over-spray."
    }
}

# ---------------------------------------------------------
#                 RULE ENGINE
# ---------------------------------------------------------
def rule_engine(input_dict):
    soil = input_dict["Soil_feel"]
    water = input_dict["Field_water"]
    insects = input_dict["Insects_seen"]
    leaf = input_dict["Leaf_condition"]
    wind = input_dict["Wind_condition"]
    weather = input_dict["Weather"]

    reasons = []
    score = 0

    if insects in ["Many", "Few"]:
        score += 2
        reasons.append("Insects visible on field")

    if leaf in ["Holes / eaten", "Spots / color change", "Curled leaves"]:
        score += 2
        reasons.append("Leaf damage detected")

    if weather == "Heavy rain":
        reasons.append("Heavy rain — unsafe for spray")
        return "No Spray - Monitor", reasons, 0.10

    if wind == "Strong":
        reasons.append("Strong wind — spray drift risk")
        return "No Spray - Monitor", reasons, 0.20

    if soil in ["Dry", "Hard-Dry"]:
        score += 1
        reasons.append("Soil moisture low")

    if water in ["Low", "Very low"]:
        score += 1
        reasons.append("Field water level low")

    if score >= 4:
        return "Spray (patch only)", reasons, 0.75
    if 2 <= score < 4:
        return "Monitor & Spot-Treat", reasons, 0.55

    return "No Spray - Monitor", reasons, 0.35

# ---------------------------------------------------------
#            CONFIDENCE FUSION (CCI)
# ---------------------------------------------------------
def compute_cci(rule_conf, ml_conf):
    return round((0.40 * rule_conf + 0.60 * ml_conf), 2)

# ---------------------------------------------------------
#          ADVICE CARD (ENSEMBLE UPDATED)
# ---------------------------------------------------------
def print_farmer_card(user_inputs, final_action, cci, rule_reasons, ml_prob, FIELD_ID, ai_info=None):
    print("\n-----------------------------------------------------------")
    print("              FARM-SENSE X ADVICE CARD               ")
    print("-----------------------------------------------------------")

    now = datetime.now()
    print(f"Date        : {now.strftime('%d-%b-%Y')}")
    print(f"Time        : {now.strftime('%I:%M %p')}")
    print(f"Field ID    : {FIELD_ID}\n")

    # --- NAYA AI SECTION ---
    if ai_info:
        disease, conf, risk = ai_info
        print(f"AI ANALYSIS : {disease}")
        print(f"AI Confidence: {conf*100:.1f}% ({risk})")
        print("-" * 30)

    print(f"Crop        : {user_inputs['Crop']} ({user_inputs['Crop_stage']} stage)")
    print(f"Soil        : {user_inputs['Soil_feel']} | Water: {user_inputs['Field_water']}")
    print(f"Insects     : {user_inputs['Insects_seen']} | Leaves: {user_inputs['Leaf_condition']}")
    print(f"Weather     : {user_inputs['Weather']} | Wind: {user_inputs['Wind_condition']}\n")

    print("Recommended Action for Farmer:")
    if final_action == "Spray (patch only)":
        print("→ Spray only on affected zones.")
        print("→ Follow pesticide bottle dose.")
        print("→ Avoid irrigation for 6 hours.")
    elif final_action == "Monitor & Spot-Treat":
        print("→ Treat only affected patches.")
        print("→ Re-inspect in next 12–36 hours.")
    else:
        print("→ No spray needed.")
        print("→ Continue regular monitoring.")

    print(f"\nSystem Confidence (CCI): {cci*100:.1f}%")

    # Timeline Recommendations
    spray_window = "10:00 AM — 4:00 PM" if user_inputs["Weather"] != "Heavy rain" and user_inputs["Wind_condition"] != "Strong" else "❌ Blocked"
    next_check = "12-18 hours" if "Insects visible" in str(rule_reasons) else "36–48 hours"
    
    print("\nTimeline Recommendations:")
    print(f"• Ideal Spray Window     : {spray_window}")
    print(f"• Next Field Check       : {next_check}")

    # Explanation Layer
    print("\nSystem Explanation:")
    if rule_reasons:
        for r in rule_reasons: print(f" - {r}")
    print(f"• ML Confidence: {ml_prob:.2f}")
    print("• Status: Rule & ML aligned" if cci > 0.6 else "• Status: System handled conflict")
    print("-----------------------------------------------------------\n")

# ---------------------------------------------------------
#          TECHNICAL REPORT (RESEARCH GRADE)
# ---------------------------------------------------------
def print_technical_section(rule_action, rule_conf, rule_reasons,
                            ml_action, ml_prob, final_action, cci, ai_info=None):
    print("\n============================================================")
    print("                   TECHNICAL REPORT")
    print("============================================================\n")

    if ai_info:
        print(f"Vision Layer (Ensemble AI):")
        print(f" - Detected: {ai_info[0]}")
        print(f" - Ensemble Probability: {ai_info[1]:.4f}")
        print("")

    print("Rule Engine (Heuristics):")
    print(f" - Decision: {rule_action} | Conf: {rule_conf}")

    print("\nCalibrated ML (XGBoost):")
    print(f" - Decision: {ml_action} | Prob: {ml_prob:.3f}")

    print("\nHybrid Fusion Strategy:")
    print(f" - Final Label: {final_action}")
    print(f" - CCI Score (Weighted 40/60): {cci}")
    print("\n============================================================\n")

def ask_choice(prompt, options):
    print(f"\n{prompt}")
    for i, op in enumerate(options, 1):
        print(f"{i}. {op}")
    return options[int(input("Enter number: ")) - 1]

def get_live_weather(city):
    """Satellite API se weather fetch karega"""
    API_KEY = "8bc803e7a0364d975871f3014a0656a1" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": f"{data['main']['temp']}°C", 
                "wind": data['wind']['speed'], 
                "status": data['weather'][0]['main']
            }
    except: pass
    return None

def get_trend_analysis(farmer_name, location):
    try:
        db_path = os.path.join(ROOT, "data", "agri_sense.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''SELECT disease_detected FROM farm_logs 
                          WHERE farmer_name=? AND location=? 
                          ORDER BY timestamp DESC LIMIT 3''', (farmer_name, location))
        rows = cursor.fetchall()
        conn.close()
        alerts = [r[0] for r in rows if r[0] != "N/A"]
        if len(alerts) >= 2:
            return f"⚠️ ALERT: {farmer_name} bhai, is area mein bimari ki activity badhi hai!"
    except: pass
    return f"✅ STATUS: {farmer_name} bhai, khet stable hai."

def save_digital_receipt(farmer, loc, field_id, card_text, prescription_text):
    """Farmer ke liye .txt file banata hai"""
    folder = os.path.join(ROOT, "reports")
    os.makedirs(folder, exist_ok=True)
    file_name = f"{farmer}_{loc}_{datetime.now().strftime('%H%M%S')}.txt"
    path = os.path.join(folder, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"FARM-SENSE X REPORT\n{'='*20}\n{card_text}\n{prescription_text}")
    return path

# ---------------------------------------------------------
#                   MAIN LOGIC
# # ---------------------------------------------------------
def main():
    # Industry Standard Header
    print("\n" + "="*60)
    print("      FARM-SENSE X v2.5: HYBRID INTELLIGENCE SYSTEM")
    print("="*60 + "\n")

    # 1. DATA ACQUISITION LAYER
    farmer_name = input("Enter Farmer Name: ").strip() or "Guest Farmer"
    village_name = input("Enter Village/City Name: ").strip() or "Unknown Location"
    
    # --- 🛰️ SATELLITE WEATHER SYNC ---
    print(f"\n[System] Synchronizing with Weather Satellites for {village_name}...")
    weather_data = get_live_weather(village_name)

    # Initialize variables with defaults
    Wind = "Light"
    Weather = "Clear"

    if weather_data:
        print(f"✅ [Live Sync Success] Temp: {weather_data['temp']} | Status: {weather_data['status']}")
        # Satellite mapping logic
        Weather = "Cloudy" if "Cloud" in weather_data['status'] else "Clear"
        Wind = "Strong" if weather_data['wind'] > 5.5 else "Light"
        print(f"🤖 [Auto-Config] Data applied: Weather={Weather}, Wind={Wind}")
    else:
        print(f"⚠️  [Weather Sync Offline] Satellite API not reachable. Manual Mode active.\n")

    # 2. INPUTS (Manual inputs only if Satellite fails)
    Soil = ask_choice("Select Soil_feel:", ["Wet", "Normal", "Dry", "Hard-Dry"])
    Water = ask_choice("Select Field_water:", ["Too much", "Normal", "Low", "Very low"])
    Insects = ask_choice("Select Insects_seen:", ["Many", "Few", "None", "Not sure"])
    Leaf = ask_choice("Select Leaf_condition:", ["Holes / eaten", "Spots / color change", "Curled leaves", "Leaves normal"])
    
    # AGAR WEATHER DATA NAHI MILA, TOH HI POOCHO
    if not weather_data:
        Wind = ask_choice("Select Wind_condition:", ["Strong", "Light", "No wind"])
        Weather = ask_choice("Select Weather:", ["Clear", "Cloudy", "Light rain", "Heavy rain", "Not sure"])
    
    Crop = ask_choice("Select Crop:", ["Maize", "Wheat", "Rice", "Cotton", "Vegetables", "Other"])
    Stage = ask_choice("Select Crop_stage:", ["Early", "Mid", "Late"])
    Field = ask_choice("Select Field_size:", ["Small", "Medium", "Large"])

    # 3. VISION PATHWAY
    img_name = input("\nEnter image name (test1.png): ").strip()
    img_path = os.path.join(ROOT, "test_images", img_name) if img_name else ""
    
    FIELD_ID = "Field_" + datetime.now().strftime("%H%M%S")
    ai_info = None

    if img_path and os.path.exists(img_path):
        print(f"\n[AI] Initializing Triple-CNN Ensemble...")
        try:
            predictor = AgriEnsemble(os.path.join(MODEL_DIR, "ensemble_pest_model.pth"))
            disease, conf = predictor.predict(img_path)
            ai_info = (disease, conf, "High Risk" if conf > 0.8 else "Low Risk")
            if conf > 0.8: Leaf = "Holes / eaten"
        except Exception as e:
            print(f"AI Error: {e}")

    user_inputs = {
        "Soil_feel": Soil, "Field_water": Water, "Insects_seen": Insects,
        "Leaf_condition": Leaf, "Wind_condition": Wind, "Weather": Weather,
        "Crop": Crop, "Crop_stage": Stage, "Field_size": Field,
    }

    # 4. ANALYSIS
    rule_act, rule_reasons, rule_conf = rule_engine(user_inputs)
    mapped = map_inputs(user_inputs)
    X_test = pd.DataFrame([mapped])
    X_test = pd.get_dummies(X_test)
    for col in FEATURE_COLS:
        if col not in X_test: X_test[col] = 0
    probs = CAL_MODEL.predict_proba(X_test[FEATURE_COLS])[0]
    ml_idx = np.argmax(probs)
    ml_act, ml_prob = ENCODER.inverse_transform([ml_idx])[0], probs[ml_idx]
    cci = compute_cci(rule_conf, ml_prob)
    final_action = ml_act if cci > 0.55 else rule_act

    # 5. OUTPUT
    print_farmer_card(user_inputs, final_action, cci, rule_reasons, ml_prob, FIELD_ID, ai_info=ai_info)

    disease_key = ai_info[0] if ai_info else "Unknown"
    rec_pesticide = PESTICIDE_DB.get(disease_key, PESTICIDE_DB["Unknown"])
    
    print(f"-----------------------------------------------------------")
    print(f"            💊 EXPERT PRESCRIPTION (AI BASED)              ")
    print(f"-----------------------------------------------------------")
    print(f"➤ Chemical : {rec_pesticide['Chemical']}")
    print(f"➤ Dosage   : {rec_pesticide['Dose']}")
    print(f"➤ Organic  : {rec_pesticide['Organic']}")
    print(f"➤ Safety   : {rec_pesticide['Safety']}")
    print(f"-----------------------------------------------------------\n")

    print_technical_section(rule_act, rule_conf, rule_reasons, ml_act, ml_prob, final_action, cci, ai_info=ai_info)

    # 6. PERSISTENCE
    try:
        from database_manager import init_db, save_log
        init_db() 
        save_log(FIELD_ID, farmer_name, village_name, Crop, ai_info[0] if ai_info else "N/A", 
                 ai_info[1] if ai_info else 0.0, final_action, cci, Weather, Wind)
        
        print(f"[Database] Record for {farmer_name} archived.")
        print(f"\n[Trend Intelligence] {get_trend_analysis(farmer_name, village_name)}")
        
        parchi_text = f"Action: {final_action} | CCI: {cci*100}%"
        presc_text = f"Med: {rec_pesticide['Chemical']} | Dose: {rec_pesticide['Dose']}"
        path = save_digital_receipt(farmer_name, village_name, FIELD_ID, parchi_text, presc_text)
        print(f"📄 Digital Receipt: {path}")
    except Exception as e:
        print(f"Database Error: {e}")
    # ============================================================

def get_trend_analysis(farmer_name, location):
    """Database se pichle records check karke warning deta hai"""
    try:
        db_path = os.path.join(ROOT, "data", "agri_sense.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Query fix: insects_seen ki jagah disease_detected use karein
        cursor.execute('''SELECT disease_detected FROM farm_logs 
                  WHERE farmer_name=? AND location=? 
                  ORDER BY timestamp DESC LIMIT 3''', (farmer_name, location))
        rows = cursor.fetchall()
        conn.close()
        
        # Agar pichle 3 mein se 2 bar "N/A" ke alawa kuch mila, toh alert do
        alerts = [r[0] for r in rows if r[0] != "N/A"]
        if len(alerts) >= 2:
            return f"⚠️ ALERT: {farmer_name} bhai, is area mein pichle kuch scans mein bimari dikhi hai. Savdhan rahein!"
    except Exception as e:
        return f"✅ STATUS: Pehla record create ho raha hai."
    return f"✅ STATUS: {farmer_name} bhai, aapka khet stable hai."

def save_digital_receipt(farmer, loc, field_id, card_text, prescription_text):
    """Farmer ke liye ek .txt file (Parchi) generate karta hai"""
    folder = os.path.join(ROOT, "reports")
    os.makedirs(folder, exist_ok=True)
    file_name = f"{farmer}_{loc}_{datetime.now().strftime('%d%b')}.txt"
    path = os.path.join(folder, file_name)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("===========================================================\n")
        f.write("             FARM-SENSE X: DIGITAL PRESCRIPTION            \n")
        f.write("===========================================================\n")
        f.write(card_text)
        f.write("\n" + prescription_text)
        f.write("\nGenerated by Farm-Sense X AI Engine\n")
    return path

if __name__ == "__main__":
    from ensemble_predict import AgriEnsemble
    main()





    #C:\AGRI-SENSE-X\test_images\test1.png