import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "agri_sense.db")

def show_all_logs():
    if not os.path.exists(DB_PATH):
        print("\n[Error] Database file (agri_sense.db) nahi mili! Pehle 'run_agri_sense.py' chalayein.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # 1. Fetching all relevant startup columns
        query = """
        SELECT 
            id, farmer_name, location, timestamp, crop, 
            disease_detected, ai_confidence, final_action, cci_score 
        FROM farm_logs
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        # 2. Data Cleaning for Professional Display
        # CCI Score ko float banakar 2 decimal tak round karein
        df['cci_score'] = pd.to_numeric(df['cci_score']).round(2)
        
        # AI Confidence ko % mein badlein (agar 0.068 hai toh 6.8%)
        df['ai_conf'] = (pd.to_numeric(df['ai_confidence']) * 100).round(1).astype(str) + '%'
        
        # Original column drop karke sundar wala rakhein
        df = df.drop(columns=['ai_confidence'])

        # 3. Terminal Display Settings
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'center')

        print("\n" + "="*120)
        print("                FARM-SENSE X: MASTER DATABASE & FARMER LOGS (v2.5)")
        print("="*120)
        
        if df.empty:
            print("\n           --- No Records Found. Start scanning to build database. ---")
        else:
            print(df.to_string(index=False))

        print("="*120)

        # 4. STARTUP ANALYTICS
        print("\n[📊 SYSTEM ANALYTICS SUMMARY]")
        print(f"• Total Consultations : {len(df)}")
        print(f"• Unique Farmers      : {df['farmer_name'].nunique()}")
        print(f"• Active Locations    : {df['location'].nunique()}")
        
        top_disease = df['disease_detected'].mode()[0] if not df.empty else "N/A"
        print(f"• Most Detected Pest  : {top_disease}")
        print("="*120 + "\n")

    except Exception as e:
        print(f"\n[Database Error] Table structure mismatch: {e}")
        print("Tip: Purani 'agri_sense.db' delete karke naya scan karein.")

if __name__ == "__main__":
    show_all_logs()