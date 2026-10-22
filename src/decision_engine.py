import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple, Optional
from config import config

logger = logging.getLogger(__name__)


class RuleEngine:

    @staticmethod
    def evaluate(inputs: Dict[str, Any]) -> Tuple[str, List[str], float]:
        soil = inputs.get("Soil_feel", "Normal")
        water = inputs.get("Field_water", "Normal")
        insects = inputs.get("Insects_seen", "None")
        leaf = inputs.get("Leaf_condition", "Leaves normal")
        wind = inputs.get("Wind_condition", "Light")
        weather = inputs.get("Weather", "Clear")

        reasons: List[str] = []
        score: float = 0.0

        if insects in ["Many", "Few"]:
            score += 2.0
            reasons.append("Pest / Insect activity observed in field")

        if leaf in ["Holes / eaten", "Spots / color change", "Curled leaves"]:
            score += 2.0
            reasons.append("Visual leaf damage / symptoms detected")

        if weather == "Heavy rain":
            reasons.append("Heavy rain expected — chemical application unsafe")
            return "No Spray - Monitor", reasons, 0.10

        if wind == "Strong":
            reasons.append("High wind intensity — severe spray drift risk")
            return "No Spray - Monitor", reasons, 0.20

        if soil in ["Dry", "Hard-Dry"]:
            score += 1.0
            reasons.append("Soil moisture level critically low")

        if water in ["Low", "Very low"]:
            score += 1.0
            reasons.append("Field water index low")

        if score >= 4.0:
            action = "Spray (patch only)"
            rule_conf = 0.75
        elif 2.0 <= score < 4.0:
            action = "Monitor & Spot-Treat"
            rule_conf = 0.55
        else:
            action = "No Spray - Monitor"
            rule_conf = 0.35

        logger.debug(f"Rule Engine Evaluation: Action='{action}', Score={score}, Reasons={reasons}")
        return action, reasons, rule_conf


def simple_fusion(mapped_inputs: Dict[str, Any], ai_score: Optional[float] = None) -> Dict[str, Any]:
    reasons: List[str] = []
    score: float = 0.0

    leaf_val = ai_score if ai_score is not None else mapped_inputs.get("Leaf_condition", 0.0) or 0.0
    if leaf_val >= 0.8:
        reasons.append("Critical leaf damage (AI Confirmed)")
        score += 0.5
    elif leaf_val >= 0.5:
        reasons.append("Leaf damage detected")
        score += 0.3
    elif leaf_val >= 0.3:
        reasons.append("Minor leaf spots")
        score += 0.1

    pest_val = mapped_inputs.get("Insects_seen", 0) or 0
    if pest_val >= 15:
        reasons.append("Many insects seen")
        score += 0.4
    elif pest_val >= 5:
        reasons.append("Some insects seen")
        score += 0.2

    wind_val = mapped_inputs.get("Wind_condition", 7) or 7
    wind_safe = wind_val <= 10.0
    if not wind_safe:
        reasons.append("Wind too strong — spraying unsafe")
        score -= 1.0

    rain_val = mapped_inputs.get("Weather", 0) or 0
    if rain_val >= 10.0:
        reasons.append("Heavy rain expected — avoid spraying")
        score -= 1.0

    if score > 0.4 and wind_safe:
        action = "Spray (patch only)"
        confidence = min(0.90, 0.50 + score * 0.40)
    elif score > 0.1 and wind_safe:
        action = "Monitor & Spot-Treat"
        confidence = min(0.80, 0.40 + score * 0.30)
    else:
        action = "No Spray - Monitor"
        confidence = max(0.20, 0.30 + score * 0.20)

    now = datetime.now()
    best_window = f"{(now + timedelta(minutes=30)).strftime('%I:%M %p')} - {(now + timedelta(hours=5)).strftime('%I:%M %p')}"
    next_check = (now + timedelta(hours=36)).strftime('%Y-%m-%d %I:%M %p')

    return {
        "action": action,
        "confidence": round(confidence, 2),
        "reasons": reasons,
        "best_spray_window": best_window,
        "next_check_time": next_check
    }