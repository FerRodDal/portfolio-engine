import yfinance as yf
import pandas as pd

def get_latest_price(ticker:str) -> float:
    # Fetches the latest closing price for a given asset ticker using Yahoo Finance API.
    
    # Args:
    #     ticker (str): The symbol of the asset (e.g., 'BTC-USD', '^GSPC').
        
    # Returns:
    #     float: The latest closing price. Returns 0.0 if there is an error.

    try:
        # Create the Ticker object.
        asset = yf.Ticker(ticker)

        # Fetch the historical data for the last day.
        history_data = asset.history(period="1d")

        # Check if the dataframe is empty.
        if history_data.empty:
            print(f"[WARNING] No data found fot ticker: {ticker}")
            return 0.0
        
        # Extract the last available "Close" price.
        latest_price = float(history_data["Close"].iloc[-1])
        return round(latest_price, 2)
    
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {ticker}: {str(e)}")
        return 0.0
    
# --- Test Block ---
# This block only runs if you execute this specific file directly.
if __name__ == "__main__":
    print("Testing API Connections...")

    # Define our target assets
    # VUAA.L = Vanguard S&P 500 UCITS ETF (USD)
    # VWRA.L = Vanguard FTSE All-World UCITS ETF (USD)
    # BTC-USD = Bitcoin in USD (USD)
    target_assets = ["VUAA.L", "VWRA.L", "BTC-USD"]

    for asset_ticker in target_assets:
        price = get_latest_price(asset_ticker)
        print(f"Latest price for {asset_ticker}: {price}")
    