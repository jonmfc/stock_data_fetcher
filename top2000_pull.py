import os
import yfinance as yf
import pandas as pd
import shutil

# program can be modified to import to a database via sql alchemy and pandas
def fetch_and_save_data(stock_symbols):
    intervals = {
        # left is time period, right is interval
        # "2d": "1m", 
        # "1wk": "5m", 
        # "1mo": "1d",
        # "1y": "1d",
        # "2y": "1d", 
         "all": "1d" # all data from start 
    }

    for stock_symbol in stock_symbols:
        stock = yf.Ticker(stock_symbol)
        data_found = False  # Flag to track if any data is found
        folder_path = f'ticker_data/ticker_{stock_symbol}'  # Define folder path for CSV files
        os.makedirs(folder_path, exist_ok=True)  # Create the directory 

        for interval, data_interval in intervals.items():
            if interval != "all":
                data = stock.history(period=interval, interval=data_interval)
            else:
                data = stock.history(period="max")

            if not data.empty:
                data_found = True
                # Store dates for readable_date column
                data['readable_date'] = data.index
                # Convert the date index to Unix timestamp in milliseconds
                data.index = pd.to_datetime(data.index).astype(int) / 10**6
                data.reset_index(inplace=True) # Resets the index
                data.rename(columns={'index': 'Date'}, inplace=True) # Rename columns
                # Add ticker symbol as the first column
                data.insert(0, 'ticker', stock_symbol)

                # Save data to a CSV file
                csv_file_path = os.path.join(folder_path, f'{stock_symbol}_{interval}.csv')
                data.to_csv(csv_file_path, index=False)
                # print(f"Saved {stock_symbol} data for {interval} to CSV at {csv_file_path}")

            if not data_found:
                print(f"No data found for {stock_symbol}.")
                shutil.rmtree(folder_path)
    print("Download Completed\n")

def read_tickers_from_csv(file_path):
    data = pd.read_csv(file_path)
    #first column is tickernames
    tickers = data.iloc[:, 0].tolist()
    return tickers



file_path = 'top2000.csv'
tickers = read_tickers_from_csv(file_path)
fetch_and_save_data(tickers) # collects its data
