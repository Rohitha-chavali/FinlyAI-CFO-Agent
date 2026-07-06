import sqlite3
import datetime
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def init_db(db_path: str = "finlyai.db") -> None:
    """Initializes the SQLite database with the runs audit trail schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the audit trail table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            run_type TEXT NOT NULL,          -- 'manual' or 'scheduled'
            status TEXT NOT NULL,            -- 'SUCCESS' or 'FAILED'
            alerts_count INTEGER NOT NULL,
            po_count INTEGER NOT NULL,
            decision_json TEXT,              -- The JSON dump of Fragment 3 CFO output
            error_message TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_pipeline_run(
    db_path: str,
    run_type: str,
    status: str,
    alerts_count: int,
    po_count: int,
    decision_json: str,
    error_message: str = None
) -> int:
    """Inserts a pipeline run entry into the audit trail database. Returns the insert ID."""
    timestamp = datetime.datetime.now().isoformat()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO pipeline_runs (
                timestamp, run_type, status, alerts_count, po_count, decision_json, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, run_type, status, alerts_count, po_count, decision_json, error_message))
        conn.commit()
        last_row_id = cursor.lastrowid
        logging.info(f"Pipeline run logged successfully with ID: {last_row_id}")
        return last_row_id
    except sqlite3.Error as e:
        logging.error(f"Failed to log pipeline run in database: {e}")
        raise e
    finally:
        conn.close()


def get_pipeline_logs(db_path: str) -> List[Dict[str, Any]]:
    """Retrieves all pipeline run history from the database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    runs = []
    try:
        cursor.execute("SELECT * FROM pipeline_runs ORDER BY id DESC")
        rows = cursor.fetchall()
        for row in rows:
            runs.append(dict(row))
    except sqlite3.Error as e:
        logging.error(f"Failed to query pipeline run history: {e}")
    finally:
        conn.close()
        
    return runs
