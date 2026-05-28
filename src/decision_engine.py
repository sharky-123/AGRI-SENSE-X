from datetime import datetime, timedelta

def simple_fusion(mapped, ai_score=None):
    reasons = []
    score = 0.0

   
    leaf = ai_score if ai_score is not None else (mapped.get("Leaf_condition", 0.0) or 0.0)
    
    if leaf >= 0.8:
        reasons.append("Critical leaf damage (AI Confirmed)")
        score += 0.5  
    elif leaf >= 0.5:
        reasons.append("Leaf damage detected")
        score += 0.3
    elif leaf >= 0.3:
        reasons.append("Minor leaf spots")
        score += 0.1


    pest = mapped.get("Insects_seen", 0) or 0
    if pest >= 15:
        reasons.append("Many insects seen")
        score += 0.4
    elif pest >= 5:
        reasons.append("Some insects seen")
        score += 0.2

    
    wind = mapped.get("Wind_condition", 7) or 7
    wind_safe = wind <= 10
    if not wind_safe:
        reasons.append("Wind too strong — spraying unsafe")
        score -= 1.0

    rain = mapped.get("Weather", 0) or 0
    if rain >= 10:
        reasons.append("Heavy rain expected — avoid spraying")
        score -= 1.0

    # 4. Final decision logic
    if score > 0.4 and wind_safe:
        action = "Spray (patch only)"
        confidence = min(0.9, 0.5 + score * 0.4)
    elif score > 0.1 and wind_safe:
        action = "Monitor & Spot-Treat"
        confidence = min(0.8, 0.4 + score * 0.3)
    else:
        action = "No Spray — Monitor"
        confidence = max(0.2, 0.3 + score * 0.2)


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