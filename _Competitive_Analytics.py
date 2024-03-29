import streamlit as st
import pandas as pd
import yfinance as yf
from st_aggrid import AgGrid
import csv
from datetime import datetime
st.markdown("# Team Rankings")
st.write("Team Rankings Based on P&L From Stocks Pitched at IBOARD")

from yahoo_fin import stock_info as si
df = pd.read_csv('IBOARD.csv')
def add_current_price(df):
    # Create an empty list to store the current prices
    current_prices = []

    # Loop through the rows and get the current price for each stock
    for i, row in df.iterrows():
        symbol = row['Pitch']
        price = si.get_live_price(symbol)
        current_prices.append(price)

    # Add the current prices as a new column to the dataframe
    df['Current Price'] = current_prices

    return df
def add_price_bought_at(df):
    # Create an empty list to store the prices bought at
    prices_bought_at = []

    # Loop through the rows and get the opening price for each stock on the date listed in 'Date of Next Open' column
    for i, row in df.iterrows():
        symbol = row['Pitch']
        date = row['Date of Next Open']
        price = si.get_data(symbol, start_date=date)['open'][0]
        prices_bought_at.append(price)

    # Add the prices bought at as a new column to the dataframe
    df['Price Bought At'] = prices_bought_at

    return df

# Read in the updated dataframe

df = add_current_price(df)
df = add_price_bought_at(df)

# Calculate the percent change for each row
df['Percent Change'] = (df['Current Price'] - df['Price Bought At']) / df['Price Bought At'] * 100

# Group the dataframe by 'Team' and calculate the average percent change for each group
avg_percent_change = df.groupby('Team')['Percent Change'].mean()

# Sort the teams by their average percent change
sorted_teams = avg_percent_change.sort_values(ascending=False)

# Add a ranking column to the sorted_teams dataframe
sorted_teams = sorted_teams.reset_index()
sorted_teams.index += 1
sorted_teams.index.name = 'Rank'

# Display the teams in order of their average percent change using st.columns()
num_columns = 2
team_chunks = [sorted_teams[i:i+num_columns] for i in range(0, len(sorted_teams), num_columns)]
for chunk in team_chunks:
    col1, col2 = st.columns(2)
    with col1:
        for rank, team in chunk.iterrows():
            st.header(f"{rank}. {team['Team']}")
    with col2:
        for rank, team in chunk.iterrows():
            st.header(f"{team['Percent Change']:.2f}%")


