import os
import sys
import logging
import argparse
import requests
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List

from config import config
from mapper import map_inputs
from decision_engine import RuleEngine
from ensemble_predict import AgriEnsemble
from predict_action import TabularMLPredictor
from database_manager import DatabaseManager

os.makedirs(os.path.join(config.ROOT_DIR, "logs"), exist_ok=True)
log_file_path = os.path.join(config.ROOT_DIR, "logs", "agri_sense.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("FARM_SENSE_X")


class WeatherService:

    @staticmethod
    def fetch_live_weather(city_name: str) -> Optional[Dict[str, Any]]:
        if not city_name or city_name.strip().lower() in ["unknown location", "guest farmer", "none", ""]:
            return None

        clean_city = city_name.strip()

        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_city}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url, timeout=config.WEATHER_API_TIMEOUT)
            if geo_res.status_code == 200:
                geo_data = geo_res.json()
                if "results" in geo_data and len(geo_data["results"]) > 0:
                    location_info = geo_data["results"][0]
                    lat = location_info["latitude"]
                    lon = location_info["longitude"]
                    resolved_name = location_info.get("name", clean_city)
                    country = location_info.get("country", "")

                    weather_url = (
                        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m"
                    )
                    w_res = requests.get(weather_url, timeout=config.WEATHER_API_TIMEOUT)
                    if w_res.status_code == 200:
                        cur = w_res.json().get("current", {})
                        temp_c = cur.get("temperature_2m", 25.0)
                        humidity = cur.get("relative_humidity_2m", 50)
                        apparent_temp = cur.get("apparent_temperature", temp_c)
                        precip = cur.get("precipitation", 0.0)
                        rain = cur.get("rain", 0.0)
                        wind_kmh = cur.get("wind_speed_10m", 10.0)
                        wind_ms = round(wind_kmh / 3.6, 2)
                        wcode = cur.get("weather_code", 0)

                        if wcode == 0:
                            status_label = "Clear"
                        elif wcode in [1, 2, 3, 45, 48]:
                            status_label = "Cloudy"
                        elif wcode in [51, 53, 55, 56, 57, 61, 63]:
                            status_label = "Light rain"
                        elif wcode in [65, 66, 67, 71, 73, 75, 77, 80, 81, 82, 85, 86, 95, 96, 99] or precip > 2.0:
                            status_label = "Heavy rain"
                        else:
                            status_label = "Cloudy"

                        drift_risk_index = round(min(1.0, (wind_ms / 10.0) * 0.7 + (1.0 if precip > 0.5 else 0.0) * 0.3), 3)

                        resolved_loc_str = f"{resolved_name}, {country}" if country else resolved_name
                        weather_info = {
                            "temp": f"{temp_c}C",
                            "temp_val": temp_c,
                            "apparent_temp": f"{apparent_temp}C",
                            "humidity": f"{humidity}%",
                            "humidity_val": humidity,
                            "precipitation": f"{precip} mm",
                            "rain": f"{rain} mm",
                            "wind": wind_ms,
                            "wind_kmh": wind_kmh,
                            "status": status_label,
                            "weather_code": wcode,
                            "drift_risk_index": drift_risk_index,
                            "resolved_location": resolved_loc_str,
                            "source": "Open-Meteo High-Precision Atmospheric Satellite API"
                        }
                        logger.info(f"Live Weather Sync Successful for '{clean_city}' ({resolved_loc_str}): {weather_info}")
                        return weather_info
        except Exception as e:
            logger.warning(f"Open-Meteo weather fetch failed for '{clean_city}': {e}")

        try:
            owm_url = f"http://api.openweathermap.org/data/2.5/weather?q={clean_city}&appid={config.OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(owm_url, timeout=config.WEATHER_API_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                temp_c = data['main']['temp']
                wind_speed = data['wind']['speed']
                humidity = data['main'].get('humidity', 50)
                weather_info = {
                    "temp": f"{temp_c}C",
                    "temp_val": temp_c,
                    "apparent_temp": f"{temp_c}C",
                    "humidity": f"{humidity}%",
                    "humidity_val": humidity,
                    "precipitation": "0.0 mm",
                    "rain": "0.0 mm",
                    "wind": wind_speed,
                    "wind_kmh": round(wind_speed * 3.6, 1),
                    "status": data['weather'][0]['main'],
                    "weather_code": 0,
                    "drift_risk_index": round(min(1.0, wind_speed / 10.0), 3),
                    "resolved_location": clean_city,
                    "source": "OpenWeatherMap API"
                }
                logger.info(f"OpenWeatherMap Live Sync Successful for '{clean_city}': {weather_info}")
                return weather_info
        except Exception as e:
            logger.warning(f"OpenWeatherMap API network unreachable: {e}")

        return None


class HybridFusionEngine:

    @staticmethod
    def compute_cci(rule_confidence: float, ml_probability: float) -> float:
        cci = (config.RULE_WEIGHT * rule_confidence) + (config.ML_WEIGHT * ml_probability)
        return round(cci, 2)

    @classmethod
    def synthesize_action(
        cls,
        rule_action: str,
        rule_conf: float,
        ml_action: str,
        ml_prob: float
    ) -> Tuple[str, float]:
        cci = cls.compute_cci(rule_conf, ml_prob)
        final_action = ml_action if cci >= config.CCI_DECISION_THRESHOLD else rule_action
        return final_action, cci


class AdvisoryReporter:

    @staticmethod
    def display_farmer_card(
        user_inputs: Dict[str, Any],
        final_action: str,
        cci: float,
        rule_reasons: List[str],
        ml_prob: float,
        field_id: str,
        ai_info: Optional[Tuple[str, float, str]] = None,
        weather_data: Optional[Dict[str, Any]] = None
    ) -> None:
        now = datetime.now()
        print("\n" + "=" * 60)
        print("              FARM-SENSE X ADVICE CARD               ")
        print("=" * 60)
        print(f"Date        : {now.strftime('%d-%b-%Y')}")
        print(f"Time        : {now.strftime('%I:%M %p')}")
        print(f"Field ID    : {field_id}\n")

        if weather_data:
            print("LIVE ATMOSPHERIC TELEMETRY (Open-Meteo):")
            print(f"Location    : {weather_data.get('resolved_location', 'N/A')}")
            print(f"Temperature : {weather_data.get('temp', 'N/A')} (Feels like: {weather_data.get('apparent_temp', 'N/A')})")
            print(f"Humidity    : {weather_data.get('humidity', 'N/A')} | Rain/Precip: {weather_data.get('precipitation', '0.0 mm')}")
            print(f"Wind Speed  : {weather_data.get('wind', 'N/A')} m/s ({weather_data.get('wind_kmh', 'N/A')} km/h)")
            print(f"Drift Risk  : {weather_data.get('drift_risk_index', 0.0) * 100:.1f}%")
            print("-" * 60)

        if ai_info:
            disease, conf, risk = ai_info
            print(f"AI ANALYSIS : {disease}")
            print(f"AI Confidence: {conf * 100:.1f}% ({risk})")
            print("-" * 40)
        else:
            print("AI ANALYSIS : N/A")
            print("AI Confidence: 0.0% (Low Risk)")
            print("-" * 40)

        print(f"Crop        : {user_inputs['Crop']} ({user_inputs['Crop_stage']} stage)")
        print(f"Soil        : {user_inputs['Soil_feel']} | Water: {user_inputs['Field_water']}")
        print(f"Insects     : {user_inputs['Insects_seen']} | Leaves: {user_inputs['Leaf_condition']}")
        print(f"Weather     : {user_inputs['Weather']} | Wind: {user_inputs['Wind_condition']}\n")

        print("Recommended Action for Farmer:")
        if final_action == "Spray (patch only)":
            print(" -> Spray only on affected zones.")
            print(" -> Follow pesticide bottle dose.")
            print(" -> Avoid irrigation for 6 hours.")
        elif final_action == "Monitor & Spot-Treat":
            print(" -> Treat only affected patches.")
            print(" -> Re-inspect in next 12-36 hours.")
        else:
            print(" -> No spray needed.")
            print(" -> Continue regular monitoring.")

        print(f"\nSystem Confidence (CCI): {cci * 100:.1f}%")

        spray_window = "10:00 AM -- 4:00 PM" if user_inputs["Weather"] != "Heavy rain" and user_inputs["Wind_condition"] != "Strong" else "[BLOCKED]"
        next_check = "12-18 hours" if "Insects visible" in str(rule_reasons) else "36--48 hours"

        print("\nTimeline Recommendations:")
        print(f" - Ideal Spray Window     : {spray_window}")
        print(f" - Next Field Check       : {next_check}")

        print("\nSystem Explanation:")
        if rule_reasons:
            for r in rule_reasons:
                print(f" - {r}")
        print(f" - ML Confidence: {ml_prob:.2f}")
        print(" - Status: Rule & ML aligned" if cci > 0.60 else " - Status: System handled conflict")
        print("=" * 60 + "\n")

    @staticmethod
    def display_technical_report(
        rule_action: str,
        rule_conf: float,
        rule_reasons: List[str],
        ml_action: str,
        ml_prob: float,
        final_action: str,
        cci: float,
        ai_info: Optional[Tuple[str, float, str]] = None,
        weather_data: Optional[Dict[str, Any]] = None
    ) -> None:
        print("\n============================================================")
        print("                   TECHNICAL REPORT")
        print("============================================================\n")

        if weather_data:
            print("Live Microclimate Layer (Satellite Geocoding + Sensor Telemetry):")
            print(f" - Station Location   : {weather_data.get('resolved_location', 'N/A')}")
            print(f" - Temp / Humidity    : {weather_data.get('temp', 'N/A')} / {weather_data.get('humidity', 'N/A')}")
            print(f" - Rain / Precip Rate : {weather_data.get('precipitation', '0.0 mm')}")
            print(f" - Wind Speed & Drift : {weather_data.get('wind', 'N/A')} m/s (Drift Risk: {weather_data.get('drift_risk_index', 0.0) * 100:.1f}%)")
            print(f" - Atmospheric Source : {weather_data.get('source', 'N/A')}\n")

        if ai_info:
            print("Vision Layer (PyTorch Ensemble AI):")
            print(f" - Detected Category: {ai_info[0]}")
            print(f" - Ensemble Probability: {ai_info[1]:.4f}")
            print("")

        print("Rule Engine (Heuristics):")
        print(f" - Decision: {rule_action} | Confidence: {rule_conf:.2f}")
        if rule_reasons:
            for r in rule_reasons:
                print(f"   * {r}")

        print("\nCalibrated ML (XGBoost):")
        print(f" - Decision: {ml_action} | Probability: {ml_prob:.4f}")

        print("\nHybrid Fusion Strategy:")
        print(f" - Final Label: {final_action}")
        print(f" - CCI Score (Weighted 40/60): {cci:.2f}")
        print("\n============================================================\n")

    @staticmethod
    def generate_digital_receipt(
        farmer_name: str,
        location: str,
        field_id: str,
        card_summary: str,
        prescription_summary: str
    ) -> str:
        os.makedirs(config.REPORTS_DIR, exist_ok=True)
        file_name = f"{farmer_name}_{location}_{datetime.now().strftime('%d%b_%H%M%S')}.txt"
        receipt_path = os.path.join(config.REPORTS_DIR, file_name)

        with open(receipt_path, "w", encoding="utf-8") as f:
            f.write("===========================================================\n")
            f.write("             FARM-SENSE X: DIGITAL PRESCRIPTION            \n")
            f.write("===========================================================\n")
            f.write(f"Farmer: {farmer_name} | Location: {location} | Field ID: {field_id}\n")
            f.write(f"Date: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}\n")
            f.write("-" * 59 + "\n")
            f.write(card_summary + "\n")
            f.write(prescription_summary + "\n")
            f.write("Generated by FARM-SENSE X Advanced AI Engine\n")

        logger.info(f"Digital prescription exported to: {receipt_path}")
        return receipt_path


def ask_choice(prompt: str, options: List[str]) -> str:
    print(f"\n{prompt}")
    for i, op in enumerate(options, 1):
        print(f"{i}. {op}")
    while True:
        try:
            choice_str = input("Enter choice number: ").strip()
            choice = int(choice_str)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"Invalid option. Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Please enter a valid integer.")


def run_pipeline(
    farmer_name: str = "Guest Farmer",
    village_name: str = "Unknown Location",
    image_name: Optional[str] = None
) -> None:
    logger.info("Initializing FARM-SENSE X v2.5 Application Pipeline.")
    print("\n" + "=" * 60)
    print("      FARM-SENSE X v2.5: HYBRID INTELLIGENCE SYSTEM")
    print("=" * 60 + "\n")

    print(f"[System] Synchronizing with Weather Satellites for '{village_name}'...")
    weather_data = WeatherService.fetch_live_weather(village_name)

    wind = "Light"
    weather = "Clear"

    if weather_data:
        res_loc = weather_data.get('resolved_location', village_name)
        print(f"[Live Sync Success] Location: {res_loc} | Temp: {weather_data['temp']} | Status: {weather_data['status']} | Wind: {weather_data['wind']} m/s | Humidity: {weather_data.get('humidity', 'N/A')}")
        weather = weather_data['status']
        wind = "Strong" if weather_data['wind'] > 5.5 else "Light"
        print(f"[Auto-Config] Applied Real-Time Parameters: Weather={weather}, Wind={wind}")
    else:
        print("[Weather Sync Offline] Satellite API not reachable. Manual Mode active.\n")

    soil = ask_choice("Select Soil_feel:", ["Wet", "Normal", "Dry", "Hard-Dry"])
    water = ask_choice("Select Field_water:", ["Too much", "Normal", "Low", "Very low"])
    insects = ask_choice("Select Insects_seen:", ["Many", "Few", "None", "Not sure"])
    leaf = ask_choice("Select Leaf_condition:", ["Holes / eaten", "Spots / color change", "Curled leaves", "Leaves normal"])

    if not weather_data:
        wind = ask_choice("Select Wind_condition:", ["Strong", "Light", "No wind"])
        weather = ask_choice("Select Weather:", ["Clear", "Cloudy", "Light rain", "Heavy rain", "Not sure"])

    crop = ask_choice("Select Crop:", ["Maize", "Wheat", "Rice", "Cotton", "Vegetables", "Other"])
    stage = ask_choice("Select Crop_stage:", ["Early", "Mid", "Late"])
    field_size = ask_choice("Select Field_size:", ["Small", "Medium", "Large"])

    if image_name is None:
        img_input = input("\nEnter leaf image filename (e.g. test1.png or press Enter to skip): ").strip()
        if img_input:
            img_path = img_input if os.path.isabs(img_input) else os.path.join(config.TEST_IMAGES_DIR, img_input)
        else:
            img_path = ""
    else:
        if os.path.isabs(image_name):
            img_path = image_name
        elif os.path.exists(os.path.join(config.TEST_IMAGES_DIR, image_name)):
            img_path = os.path.join(config.TEST_IMAGES_DIR, image_name)
        else:
            img_path = image_name

    field_id = "Field_" + datetime.now().strftime("%H%M%S")
    ai_info: Optional[Tuple[str, float, str]] = None

    if img_path and os.path.exists(img_path):
        print("\n[AI] Initializing Triple-CNN Vision Ensemble...")
        try:
            vision_predictor = AgriEnsemble()
            disease, conf = vision_predictor.predict(img_path)
            if disease != "N/A":
                risk_level = "High Risk" if conf >= config.HIGH_RISK_AI_THRESHOLD else "Low Risk"
                ai_info = (disease, conf, risk_level)
                if conf >= config.HIGH_RISK_AI_THRESHOLD:
                    leaf = "Holes / eaten"
        except Exception as e:
            logger.error(f"Vision ensemble classification failed: {e}")
            print(f"[AI Error] Vision classification issue: {e}")

    user_inputs = {
        "Soil_feel": soil, "Field_water": water, "Insects_seen": insects,
        "Leaf_condition": leaf, "Wind_condition": wind, "Weather": weather,
        "Crop": crop, "Crop_stage": stage, "Field_size": field_size,
    }

    rule_act, rule_reasons, rule_conf = RuleEngine.evaluate(user_inputs)

    ml_predictor = TabularMLPredictor()
    ml_act, ml_prob = ml_predictor.predict(user_inputs, ai_score=ai_info[1] if ai_info else None)

    final_action, cci = HybridFusionEngine.synthesize_action(rule_act, rule_conf, ml_act, ml_prob)

    AdvisoryReporter.display_farmer_card(user_inputs, final_action, cci, rule_reasons, ml_prob, field_id, ai_info=ai_info, weather_data=weather_data)

    disease_key = ai_info[0] if ai_info else "Unknown"
    rec_pesticide = config.query_pesticide(disease_key)

    print("-----------------------------------------------------------")
    print("            EXPERT PRESCRIPTION (AI BASED)                 ")
    print("-----------------------------------------------------------")
    print(f"-> Target    : {disease_key}")
    print(f"-> Chemical : {rec_pesticide['Chemical']}")
    print(f"-> Dosage   : {rec_pesticide['Dose']}")
    print(f"-> Organic  : {rec_pesticide['Organic']}")
    print(f"-> Safety   : {rec_pesticide['Safety']}")
    print("-----------------------------------------------------------\n")

    AdvisoryReporter.display_technical_report(rule_act, rule_conf, rule_reasons, ml_act, ml_prob, final_action, cci, ai_info=ai_info, weather_data=weather_data)

    try:
        db_mgr = DatabaseManager()
        disease_label = ai_info[0] if ai_info else "N/A"
        disease_conf = ai_info[1] if ai_info else 0.0

        db_mgr.save_log(
            field_id, farmer_name, village_name, crop,
            disease_label, disease_conf, final_action, cci, weather, wind
        )

        recent_records = db_mgr.fetch_recent_disease_records(farmer_name, village_name, limit=3)
        disease_alerts = [r for r in recent_records if r != "N/A"]

        if len(disease_alerts) >= 2:
            trend_msg = f"[ALERT] Attention {farmer_name}, recent scans indicate active disease presence in {village_name}. Please inspect crops carefully!"
        else:
            trend_msg = f"[STATUS] Field conditions stable for {farmer_name} in {village_name}."

        print(f"[Database] Record for farmer '{farmer_name}' archived.")
        print(f"\n[Trend Intelligence] {trend_msg}")

        card_summary = f"Action: {final_action} | CCI: {cci * 100:.1f}% | Weather: {weather} | Wind: {wind}"
        prescription_summary = f"Target: {disease_key} | Med: {rec_pesticide['Chemical']} | Dose: {rec_pesticide['Dose']}"
        receipt_path = AdvisoryReporter.generate_digital_receipt(farmer_name, village_name, field_id, card_summary, prescription_summary)
        print(f"[Digital Receipt]: {receipt_path}\n")

    except Exception as e:
        logger.error(f"Persistence layer error: {e}", exc_info=True)
        print(f"[Database Error] Persistence failed: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="FARM-SENSE X v2.5 Production Application")
    parser.add_argument("--farmer", type=str, default=None, help="Farmer Name")
    parser.add_argument("--city", type=str, default=None, help="Village/City Location")
    parser.add_argument("--image", type=str, default=None, help="Leaf Image filename or path")
    parser.add_argument("--non-interactive", action="store_true", help="Run in non-interactive mode")

    args = parser.parse_args()

    if args.farmer is not None or args.city is not None or args.non_interactive:
        farmer_name = args.farmer if args.farmer else "Guest Farmer"
        village_name = args.city if args.city else "Unknown Location"
    else:
        farmer_name = input("Enter Farmer Name [Default: Guest Farmer]: ").strip() or "Guest Farmer"
        village_name = input("Enter Village/City Name [Default: Unknown Location]: ").strip() or "Unknown Location"

    run_pipeline(farmer_name=farmer_name, village_name=village_name, image_name=args.image)


if __name__ == "__main__":
    main()