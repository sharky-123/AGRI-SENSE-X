import sqlite3
from datetime import datetime
import os

# Database Path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "agri_sense.db")

def init_db():
    """Database aur Table create karta hai agar exist nahi karti"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Naye startup-ready columns: farmer_name aur location
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farm_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id TEXT,
            timestamp TEXT,
            farmer_name TEXT,     
            location TEXT,        
            crop TEXT,
            disease_detected TEXT,
            ai_confidence TEXT,
            final_action TEXT,
            cci_score TEXT,
            weather TEXT,
            wind TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_log(field_id, farmer, loc, crop, disease, conf, action, cci, weather, wind):
    """Naya farm record database mein save karta hai"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO farm_logs 
            (field_id, timestamp, farmer_name, location, crop, disease_detected, ai_confidence, final_action, cci_score, weather, wind)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (field_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
              farmer, loc, crop, disease, str(conf), action, str(cci), weather, wind))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Manager Error] Data save nahi ho paya: {e}")

