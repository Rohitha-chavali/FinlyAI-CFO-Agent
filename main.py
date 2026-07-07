#!/usr/bin/env python3
"""
FinlyAI — Autonomous Virtual CFO Agent Orchestrator
Takeover Hackathon 2026
"""

import os
import sys
import time
import argparse
import json
import logging
from dotenv import load_dotenv

import inventory
import billing
import cfo
import database

# Load environment variables
load_dotenv()

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("finlyai.log", encoding="utf-8")
    ]
)

# Shared Mock Cash Position (matching original prototype)
MOCK_CASH_POSITION = {
    "cash_on_hand": 18500.00,
    "accounts_receivable_due_14d": 6200.00,
    "accounts_payable_due_14d": 3100.00,
    "avg_daily_burn": 420.00,
}


def run_pipeline(
    csv_path: str = "inventory.csv",
    output_pos_dir: str = "output_pos",
    db_path: str = "finlyai.db",
    run_type: str = "manual"
) -> bool:
    """Runs the full FinlyAI CFO fragments pipeline and logs the results."""
    logging.info(f"Starting FinlyAI pipeline run ({run_type})...")
    
    # Initialize SQLite database
    database.init_db(db_path)
    
    alerts = []
    drafts = []
    analysis = {}
    
    try:
        # Fragment 1: Inventory Tracker
        inv_data = inventory.load_inventory_from_csv(csv_path)
        alerts = inventory.run_inventory_tracker(inv_data)
        
        # Fragment 2: Automated Billing
        drafts = billing.run_automated_billing(alerts)
        
        # Fragment 3: AI CFO Agent
        analysis = cfo.run_cfo_agent(drafts, MOCK_CASH_POSITION)
        
        # Log to Database as SUCCESS
        database.log_pipeline_run(
            db_path=db_path,
            run_type=run_type,
            status="SUCCESS",
            alerts_count=len(alerts),
            po_count=len(drafts),
            decision_json=json.dumps(analysis),
            error_message=None
        )
        logging.info("FinlyAI pipeline run completed successfully.")
        return True

    except Exception as e:
        error_msg = str(e)
        logging.error(f"FinlyAI pipeline run failed: {error_msg}")
        
        # Log to Database as FAILED
        try:
            database.log_pipeline_run(
                db_path=db_path,
                run_type=run_type,
                status="FAILED",
                alerts_count=len(alerts),
                po_count=len(drafts),
                decision_json=None,
                error_message=error_msg
            )
        except Exception as db_err:
            logging.error(f"Failed to log error to sqlite: {db_err}")
            
        return False

def run_pipeline_api(
    csv_path: str = "inventory.csv",
    output_pos_dir: str = "output_pos",
    db_path: str = "finlyai.db",
):
    """
    Runs the pipeline and returns structured data for the API.
    """

    logging.info("Running FinlyAI API pipeline...")

    database.init_db(db_path)

    alerts = []
    drafts = []

    try:
        inv_data = inventory.load_inventory_from_csv(csv_path)
        alerts = inventory.run_inventory_tracker(inv_data)

        drafts = billing.run_automated_billing(alerts)

        analysis = cfo.run_cfo_agent(
            drafts,
            MOCK_CASH_POSITION
        )

        database.log_pipeline_run(
            db_path=db_path,
            run_type="api",
            status="SUCCESS",
            alerts_count=len(alerts),
            po_count=len(drafts),
            decision_json=json.dumps(analysis),
            error_message=None,
        )

        return {
            "success": True,
            "alerts": alerts,
            "purchaseOrders": drafts,
            "cashPosition": MOCK_CASH_POSITION,
            "analysis": analysis,
        }

    except Exception as e:

        error_msg = str(e)

        database.log_pipeline_run(
            db_path=db_path,
            run_type="api",
            status="FAILED",
            alerts_count=len(alerts),
            po_count=len(drafts),
            decision_json=None,
            error_message=error_msg,
        )

        return {
            "success": False,
            "error": error_msg,
        }

def run_scheduler(interval_minutes: float, csv_path: str, output_pos_dir: str, db_path: str):
    """Starts the scheduler loop, running the pipeline every N minutes."""
    try:
        import schedule
    except ImportError:
        logging.error("The 'schedule' library is not installed. Run: pip install schedule")
        sys.exit(1)
        
    logging.info(f"Initializing scheduler. Running FinlyAI pipeline every {interval_minutes} minute(s).")
    
    # Run once at startup
    run_pipeline(csv_path=csv_path, output_pos_dir=output_pos_dir, db_path=db_path, run_type="scheduled")
    
    # Schedule subsequent runs
    schedule.every(interval_minutes).minutes.do(
        run_pipeline,
        csv_path=csv_path,
        output_pos_dir=output_pos_dir,
        db_path=db_path,
        run_type="scheduled"
    )
    
    logging.info("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")


def print_history(db_path: str):
    """Queries and prints the pipeline runs audit trail history."""
    database.init_db(db_path)
    runs = database.get_pipeline_logs(db_path)
    if not runs:
        print("No run records found in the audit database.")
        return
        
    print("\n========================= PIPELINE RUN AUDIT HISTORY =========================")
    print(f"{'ID':<4} | {'Timestamp':<26} | {'Run Type':<10} | {'Status':<8} | {'Alerts':<6} | {'POs':<4}")
    print("-" * 75)
    for run in runs:
        print(f"{run['id']:<4} | {run['timestamp']:<26} | {run['run_type']:<10} | {run['status']:<8} | {run['alerts_count']:<6} | {run['po_count']:<4}")
    print("==============================================================================\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FinlyAI Orchestrator")
    parser.add_argument("--csv", default="inventory.csv", help="Path to inventory CSV file")
    parser.add_argument("--output-pos", default="output_pos", help="Directory to save generated PDF POs")
    parser.add_argument("--db", default="finlyai.db", help="Path to SQLite database file")
    parser.add_argument("--schedule", action="store_true", help="Run in schedule mode using the schedule interval")
    parser.add_argument("--interval", type=float, help="Override schedule interval (minutes)")
    parser.add_argument("--history", action="store_true", help="Print audit logs history from SQLite database")
    
    args = parser.parse_args()
    
    if args.history:
        print_history(args.db)
        sys.exit(0)
        
    if args.schedule:
        # Load interval from .env or override arg or default
        env_interval = os.getenv("SCHEDULE_INTERVAL_MINUTES")
        interval = args.interval
        if interval is None:
            if env_interval:
                try:
                    interval = float(env_interval)
                except ValueError:
                    logging.warning(f"Invalid SCHEDULE_INTERVAL_MINUTES '{env_interval}' in env. Using default 5.0")
                    interval = 5.0
            else:
                interval = 5.0
        
        run_scheduler(interval, args.csv, args.output_pos, args.db)
    else:
        # Run one-off
        success = run_pipeline(csv_path=args.csv, output_pos_dir=args.output_pos, db_path=args.db, run_type="manual")
        sys.exit(0 if success else 1)
