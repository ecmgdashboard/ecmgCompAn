import streamlit as st
import yfinance as yf
from datetime import datetime
from yahoo_fin import stock_info as si
import csv
import pandas as pd


analystdf = pd.read_csv('Comp An Analyst Pitch Holdings - Sheet1 (1).csv')
# create dropdown
analystname = analystdf.loc[:, ["Analyst Name"]]
option = st.selectbox("Select An Analyst",
             analystname)

# selected analyst pitch
pitch = analystdf.loc[analystdf['Analyst Name'] == option]
st.write(pitch)