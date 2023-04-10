import streamlit as st
import yfinance as yf
from datetime import datetime
from yahoo_fin import stock_info as si
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

    selected_analyst_df = analystdf.loc[analystdf['Analyst Name'] == option]
    tickers = tuple(selected_analyst_df['Stock'])

    # dropdown of analyst ticker
    dropdown = st.multiselect('Select Ticker(s)', tickers)
    start = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
    end = st.date_input('End', value=pd.to_datetime('today'))


    def relative_return(df):
        rel = df.pct_change()
        cumulative_return = (1 + rel).cumprod() - 1
        cumulative_return = cumulative_return.fillna(0)
        # remove MultiIndex
        cumulative_return.columns = cumulative_return.columns.droplevel()
        return cumulative_return


    if dropdown:
        st.subheader("Daily Market")
        df = yf.download(dropdown, start, end)['Adj Close']
        st.line_chart(df)
        st.subheader("Relative Returns")
        df1 = relative_return(yf.download(dropdown, start, end)['Adj Close'])
        st.line_chart(df1)
