import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_KEY = "25CSW4MZCC9FQGB1"

st.title('Stock App')

symbol = st.text_input('Enter stock symbol', value='AAPL')

start_date = st.date_input('Start date', value=datetime.today() - timedelta(days=365))
end_date = st.date_input('End date', value=datetime.today())

technical_indicators = st.multiselect(
    'Select technical indicators',
    options=['SMA', 'EMA', 'MACD', 'RSI'],
    default=['SMA', 'EMA']
)

def get_technical_indicator_data(symbol, indicator):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": indicator,
        "symbol": symbol.strip(),
        "apikey": API_KEY
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        st.write(f"Failed to fetch {indicator} data for {symbol}: HTTP {response.status_code}")
        return None

    data = response.json()

    key = f'Technical Analysis: {indicator}'
    if key not in data:
        st.write(f"No {indicator} data found for {symbol}")
        return None
    
    indicator_data = pd.DataFrame.from_dict(data[key], orient='index')
    indicator_data = indicator_data.sort_index()

    indicator_data[indicator] = indicator_data[indicator].apply(pd.to_numeric)
    
    return indicator_data

data_frames = []
for indicator in technical_indicators:
    data_frame = get_technical_indicator_data(symbol, indicator)
    if data_frame is not None:
        data_frames.append(data_frame)

if data_frames:
    data = pd.concat(data_frames, axis=1)
    data = data.loc[start_date:end_date]
    
    plt.figure(figsize=(10, 5))
    
    for indicator in technical_indicators:
        if indicator in data.columns:
            plt.plot(data.index, data[indicator], label=f'{symbol} {indicator}')
    
    plt.legend()
    plt.grid()
    st.pyplot(plt.cla())
