import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_KEY = "25CSW4MZCC9FQGB1"

st.title('Stock App')

symbols = st.text_input('Enter stock symbols (comma separated)', value='AAPL,GOOGL,MSFT')

symbols = symbols.split(',')

# Fetch daily adjusted stock data and SMA from Alpha Vantage
def get_stock_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol.strip(),
        "apikey": API_KEY
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if "Error Message" in data:
        st.write(f"Failed to fetch data for {symbol}")
        return None
    
    stock_data = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    stock_data = stock_data.sort_index()
    
    params["function"] = "SMA"
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if "Error Message" in data:
        st.write(f"Failed to fetch SMA data for {symbol}")
        return None
    
    sma_data = pd.DataFrame.from_dict(data['Technical Analysis: SMA'], orient='index')
    sma_data = sma_data.sort_index()
    
    merged_data = stock_data.join(sma_data, lsuffix='_stock', rsuffix='_sma')
    merged_data[['5. adjusted close', 'SMA']] = merged_data[['5. adjusted close', 'SMA']].apply(pd.to_numeric)
    
    return merged_data

for symbol in symbols:
    data = get_stock_data(symbol)
    
    if data is not None:
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['5. adjusted close'], label=f'{symbol} adjusted close')
        plt.plot(data.index, data['SMA'], label=f'{symbol} SMA')
        plt.legend()
        plt.grid()
        st.pyplot(plt.cla())
