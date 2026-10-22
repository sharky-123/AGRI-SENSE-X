import sqlite3
import os
import logging
from datetime import datetime
from typing import List
from config import config

logger = logging.getLogger(__name__)

class DatabaseManager:

    def __init__(self, db_path: str = config.DB_PATH) -> None:
        self.db_path = db_path
        self._ensure_db_dir()
        self.init_db()

    def _ensure_db_dir(self) -> None:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS farm_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        field_id TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        farmer_name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        crop TEXT NOT NULL,
                        disease_detected TEXT DEFAULT 'N/A',
                        ai_confidence TEXT DEFAULT '0.0',
                        final_action TEXT NOT NULL,
                        cci_score TEXT NOT NULL,
                        weather TEXT DEFAULT 'N/A',
                        wind TEXT DEFAULT 'N/A'
                    )
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_farmer_location 
                    ON farm_logs(farmer_name, location)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_timestamp 
                    ON farm_logs(timestamp DESC)
                """)
                conn.commit()
                logger.info("Database schema and indexes initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database schema: {e}", exc_info=True)
            raise

    def save_log(
        self,
        field_id: str,
        farmer_name: str,
        location: str,
        crop: str,
        disease_detected: str,
        ai_confidence: float,
        final_action: str,
        cci_score: float,
        weather: str,
        wind: str
    ) -> bool:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO farm_logs 
            (field_id, timestamp, farmer_name, location, crop, disease_detected, ai_confidence, final_action, cci_score, weather, wind)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            field_id,
            timestamp,
            farmer_name,
            location,
            crop,
            disease_detected,
            str(ai_confidence),
            final_action,
            str(cci_score),
            weather,
            wind
        )

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                logger.info(f"Successfully archived consultation record for field '{field_id}' (Farmer: {farmer_name}).")
                return True
        except sqlite3.Error as e:
            logger.error(f"Database insertion error for field '{field_id}': {e}", exc_info=True)
            return False

    def fetch_recent_disease_records(
        self, 
        farmer_name: str, 
        location: str, 
        limit: int = 3
    ) -> List[str]:
        query = """
            SELECT disease_detected FROM farm_logs 
            WHERE farmer_name = ? AND location = ? 
            ORDER BY timestamp DESC LIMIT ?
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (farmer_name, location, limit))
                rows = cursor.fetchall()
                return [row["disease_detected"] for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Database query error during outbreak analysis for {farmer_name}: {e}")
            return []


db_manager = DatabaseManager()

def init_db() -> None:
    db_manager.init_db()

def save_log(field_id: str, farmer: str, loc: str, crop: str, disease: str, conf: float, action: str, cci: float, weather: str, wind: str) -> bool:
    return db_manager.save_log(field_id, farmer, loc, crop, disease, conf, action, cci, weather, wind)
