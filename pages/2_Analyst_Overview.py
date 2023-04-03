import streamlit as st
import yfinance as yf
from datetime import datetime
from yahoo_fin import stock_info as si
import csv
import pandas as pd
from st_aggrid import AgGrid

st.header('Analyst Analyzer')
analystdf = pd.read_csv('Comp An Analyst Pitch Holdings - Sheet1 (1).csv')
# create dropdown
def current(ticker):
    try:
        stock = yf.Ticker(ticker)
        return int(stock.info['regularMarketPrice'])
    except:
        return 0

def find_analyst_stocks(name):
    analyst_df = analystdf[analystdf["Analyst Name"] == name]
    if analyst_df['Stock'].isnull().values.any():

        return 'Nothing'
    else:
        stock_str = ", ".join(analyst_df['Stock'].tolist())
        return stock_str



analystdf["Current Price"] = analystdf["Stock"].apply(current)
analystname = analystdf.loc[:, ["Analyst Name"]]
option = st.selectbox("Select An Analyst",
             analystname)

def apl(option):
    analystframe = analystdf[analystdf["Analyst Name"] == option]

# selected analyst pitch

if st.button('Analyze'):
    st.subheader(f"{option}'s Pitches Analzed")
    pitch = analystdf.loc[analystdf['Analyst Name'] == option]
    if find_analyst_stocks(option) != "None":
        pitched = find_analyst_stocks(option)
    else:
        pitched = find_analyst_stocks(option)
    st.write(f"{option} has pitched: {pitched}")

    AgGrid(pitch, height=100)

