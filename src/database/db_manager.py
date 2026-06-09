import sqlite3
import os

# Define the path where the database file will be stored
DB_PATH = os.path.join(os.path.dirname(__file__), "portfolio.db")

def init_db():
    """
    Initializes the SQLite database and creates the necessary tables 
    if they do not exist (v1.0 schema).
    """
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute the SQL script to build the relational structure
    cursor.executescript("""-- Table 1: Users
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Table 2: Portfolios
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        -- Table 3: Assets Catalog
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL
        );

        -- Table 4: Portfolio Positions and Targets
        CREATE TABLE IF NOT EXISTS portfolio_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id INTEGER NOT NULL,
            asset_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            target_weight REAL NOT NULL,
            FOREIGN KEY (portfolio_id) REFERENCES portfolios (id),
            FOREIGN KEY (asset_id) REFERENCES assets (id)
        );

        -- Table 5: Historical Prices
        CREATE TABLE IF NOT EXISTS historical_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            date DATE NOT NULL,
            close_price REAL NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES assets (id)
        );
    """)
    
    # Commit the changes and close the connection safely
    conn.commit()
    conn.close()
    print(f"[SUCCESS] Database initialized successfully at: {DB_PATH}")

# --- Test Block ---
if __name__ == "__main__":
    init_db()