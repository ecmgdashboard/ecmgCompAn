import streamlit as st
import yfinance as yf
from datetime import datetime
from yahoo_fin import stock_info as si

# Specify the ticker symbol and date as a string in Y-M-D format
ticker = "AAPL"
date_str = "2022-01-01"

# Convert the date string to a datetime object
date = datetime.strptime(date_str, "%Y-%m-%d")

# Download the stock data for the specified date
data = si.get_data(ticker,start_date=date)
x = data['open'][0]
x =round(x,2)

# Print the stock data
st.write(x)
