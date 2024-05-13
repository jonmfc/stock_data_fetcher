# Fetches entire history of a single stock 
import yfinance as yf
import pandas as pd

def fetch_and_save_stock_data(stock_symbol):
    # Fetch historical stock data
    stock_data = yf.Ticker(stock_symbol).history(period="max")
    # Unix date
    stock_data.index = pd.to_datetime(stock_data.index).astype(int) / 10**6
    stock_data['readable_date'] = pd.to_datetime(stock_data.index, unit='ms')
    # save the data
    stock_data.to_csv(f'ticker_{stock_symbol}.csv')

# Example usage
stock_symbol = input("Enter a stock symbol: ")
fetch_and_save_stock_data(stock_symbol)
