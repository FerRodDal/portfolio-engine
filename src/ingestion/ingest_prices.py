import sqlite3
import os
import sys
from datetime import datetime

# Path adjustment to allow importing local modules seamlessly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion.api_client import get_latest_price

# Direct path to the database file located in src/database/
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/portfolio.db"))

def setup_default_assets(cursor):
    """
    Inserts default assets into the catalog if they do not exist yet.
    This prevents Foreign Key violations when storing prices.
    """
    default_assets = [
        ("VUAA.L", "ETF"),
        ("VWRA.L", "ETF"),
        ("BTC-USD", "CRYPTO")
    ]

    for ticker, asset_type in default_assets:
        cursor.execute("""
            INSERT OR IGNORE INTO assets (ticker, type)
            VALUES (?, ?)
        """, (ticker, asset_type))

def ingest_current_prices():
    """
    Main pipeline: Fetches live prices, cleans/validates them, 
    and saves them into the historical_prices table.
    """
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database file not found at {DB_PATH}. Please run db.manager.py first.")
        return
    
    # Open database connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 1: Ensure asstes are registered in the catalog
    setup_default_assets(conn)
    conn.commit()

    # Define targets and get current timestamp
    target_assets = ["VUAA.L", "VWRA.L", "BTC-USD"]
    today_date = datetime.now().strftime("%Y-%m-%d")

    print(f"--- Starting Price Ingestion Pipeline ({today_date}) ---")

    for ticker in target_assets:
        # Step 2: Extract data from public API
        price = get_latest_price(ticker)

        # Step 3: Data Cleaning & Validation (Error Handling)
        if price <= 0.0:
            print(f"[DATA CLEANING] [WARNING] Invalid price (${price}) for {ticker}. Data discarded.")
            continue

        # Step 4: Fetch the internal asset ID
        cursor.execute("SELECT id FROM assets WHERE ticker = ?", (ticker,))
        asset_id = cursor.fetchone()[0]

        # Step 5: Load clean data into historical_prices table
        cursor.execute("""
            INSERT INTO historical_prices (asset_id, date, close_price)
            VALUES (?, ?, ?)
        """, (asset_id, today_date, price))

        print(f"[LOAD] [SUCCESS] Saved {ticker} (ID: {asset_id}) price: ${price}")

    # Commit transactions and close connection safely
    conn.commit()
    conn.close()
    print("--- Price Ingestion Pipeline Finished Successfully ---")

if __name__ == "__main__":
    ingest_current_prices()