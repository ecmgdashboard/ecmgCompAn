import streamlit as st
import yfinance as yf
from datetime import datetime
from yahoo_fin import stock_info as si
import pandas as pd
from st_aggrid import AgGrid

st.header('Analyst Analyzer')
analystdf = pd.read_csv('Individual Analyst Stock Pitches - Sheet1.csv')

list_stocks = []

def current(ticker):
    try:
        stock = yf.Ticker(ticker)
        return int(stock.info['regularMarketPrice'])
    except:
        return 0

def find_analyst_stocks(name):
    analyst_df = analystdf[analystdf["Analyst Name"] == name]
    if analyst_df['Stock'].isnull().values.any():
        return 'No Stock'
    else:
        stock_str = ", ".join(analyst_df['Stock'].tolist())
        return analyst_df['Stock'].tolist()

def find_analyst_stock_enter(name, stock):
    analyst_df = analystdf[analystdf["Analyst Name"] == name]
    stock_enter = analyst_df['Entry Date'].tolist()
    return stock_enter

analystdf["Current Price"] = analystdf["Stock"].apply(current)
analystname = analystdf.loc[:, ["Analyst Name"]]
option = st.selectbox("Select An Analyst", analystname)

if st.button('Analyze'):
    st.subheader(f"{option}'s Pitches Analyzed")
    pitch = analystdf.loc[analystdf['Analyst Name'] == option]
    selected_tickers = find_analyst_stocks(option)
    if selected_tickers:
        list_stocks.extend(selected_tickers)
        pitched = ", ".join(selected_tickers)
    else:
        pitched = "No Stock"
    st.write(f"{option} has pitched: {pitched}")
    AgGrid(pitch, height=100)

    selected_analyst_df = analystdf.loc[analystdf['Analyst Name'] == option]
    tickers = tuple(selected_analyst_df['Stock'])

   # end = st.date_input('End', value=pd.to_datetime('today'))

    def relative_return(df):
        rel = df.pct_change()
        cumulative_return = (1 + rel).cumprod()-1
        cumulative_return = cumulative_return.fillna(0)
        # remove MultiIndex
        cumulative_return.columns = cumulative_return.columns.droplevel()
        return cumulative_return
 #   st.subheader("Daily Market")
 #   stock_data = pd.DataFrame()
  #  for stock in tickers:
  #      start = pd.to_datetime(find_analyst_stock_enter(option, stock))
   #     df = yf.download(stock, start, end)['Adj Close']
   #     stock_data = pd.concat([stock_data, df], axis=1)
  #  st.line_chart(stock_data)
with open("Individual Analyst Stock Pitches - Sheet1.csv", "r") as csv_file:
    for line in csv_file:
        def liveprice(ticker):
            current_price = si.get_live_price(ticker)
            current_price = round(current_price, 2)
            # round(current_price,5)
            return current_price


        if option in line:
            stock = find_analyst_stocks(option)
            values = line.split(',')
            purchaseprice = values[4]
            currentprice = liveprice(values[3])

            if pd.notnull(purchaseprice) and purchaseprice != '':
                purchaseprice = float(purchaseprice)

                if purchaseprice > 0:
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)
                    st.metric(label="PnL", value=f'{change}%')
                else:
                    st.write('No PnL Calculated')
            else:
                st.write(values[3] + ': No purchase price provided')

    # Daily Market
    # df = yf.download(tickers, start, end)['Adj Close']
    # st.line
