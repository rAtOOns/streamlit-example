import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# Replace with your own API key
API_KEY = "25CSW4MZCC9FQGB1"

st.title('Enhanced SCTR Stock App')

# Input multiple stock symbols
symbols = st.text_input('Enter stock symbols (comma separated)', value='AAPL,GOOGL,MSFT')

# Convert the input to a list
symbols = symbols.split(',')

# Define a function to get technical data from the API
def get_technical_data(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol.strip()}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Iterate over the symbols
for symbol in symbols:
    data = get_technical_data(symbol)
    
    if data is not None:
        # Get the SCTR, RSI, Moving averages and MACD
        st.write(f"Technical Data for {symbol}:")
        st.write(f"SCTR: {data.get('SCTR', 'N/A')}")
        st.write(f"RSI: {data.get('RSI', 'N/A')}")
        st.write(f"Moving Average: {data.get('MovingAverage', 'N/A')}")
        st.write(f"MACD: {data.get('MACD', 'N/A')}")

        # Plot SCTR over time
        sctr_over_time = pd.DataFrame(data.get('SCTR_Historical', {}))
        plt.figure(figsize=(10, 5))
        plt.plot(sctr_over_time.index, sctr_over_time['SCTR'], label=f'{symbol} SCTR')
        plt.legend()
        plt.grid()
        st.pyplot(plt.cla())

        # Predict future trend based on historical SCTR
        model = LinearRegression()
        X = sctr_over_time.index.values.reshape(-1, 1)
        y = sctr_over_time['SCTR']
        model.fit(X, y)
        future_trend = model.predict(X)
        st.write(f"Predicted Future SCTR trend for {symbol}: {future_trend[-1]}")
    else:
        st.write(f"Failed to fetch data for {symbol}")
