import os
import sqlite3
import logging
import pandas as pd
from config import config
from database_manager import DatabaseManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("LOGS_VIEWER")


def show_all_logs(db_path: str = config.DB_PATH) -> None:
    if not os.path.exists(db_path):
        print(f"\n[Error] Database file missing at '{db_path}'. Please run 'run_agri_sense.py' first.")
        logger.error(f"Database path not found: {db_path}")
        return

    try:
        db_mgr = DatabaseManager(db_path=db_path)
        with db_mgr.get_connection() as conn:
            query = """
                SELECT 
                    id, farmer_name, location, timestamp, crop, 
                    disease_detected, ai_confidence, final_action, cci_score 
                FROM farm_logs
                ORDER BY id ASC
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            print("\n" + "=" * 110)
            print("                FARM-SENSE X: MASTER DATABASE & FARMER LOGS (v2.5)")
            print("=" * 110)
            print("\n           --- No Consultation Records Found in Database. ---")
            print("=" * 110 + "\n")
            return

        df['cci_score'] = pd.to_numeric(df['cci_score'], errors='coerce').round(2)
        df['ai_conf'] = (pd.to_numeric(df['ai_confidence'], errors='coerce').fillna(0.0) * 100).round(1).astype(str) + '%'
        df = df.drop(columns=['ai_confidence'])

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'center')

        print("\n" + "=" * 115)
        print("                FARM-SENSE X: MASTER DATABASE & FARMER LOGS (v2.5)")
        print("=" * 115)
        print(df.to_string(index=False))
        print("=" * 115)

        total_consultations = len(df)
        unique_farmers = df['farmer_name'].nunique()
        active_locations = df['location'].nunique()
        top_disease = df['disease_detected'].mode()[0] if not df.empty else "N/A"

        print("\n[SYSTEM ANALYTICS SUMMARY]")
        print(f" - Total Consultations : {total_consultations}")
        print(f" - Unique Farmers      : {unique_farmers}")
        print(f" - Active Locations    : {active_locations}")
        print(f" - Most Detected Pest  : {top_disease}")
        print("=" * 115 + "\n")

    except sqlite3.Error as e:
        logger.error(f"Database query error: {e}", exc_info=True)
        print(f"\n[Database Error] Issue executing query: {e}")
        print("Tip: If schema mismatch exists, remove old 'agri_sense.db' file and re-run application.")
    except Exception as e:
        logger.error(f"Unexpected error displaying logs: {e}", exc_info=True)
        print(f"\n[Error] Display issue: {e}")


if __name__ == "__main__":
    show_all_logs()