import csv
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import date
from datetime import datetime
from yahoo_fin import stock_info as si
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
#from streamlit_vega_lite import vega_lite_component, AltairComponent

st.markdown("# **:green[ Team Analyzer/I-Board Results :tada:]**")
st.caption('**based on IBoard pitches since 1/1/2023')

df = pd.read_csv("IBOARD.csv")

# Output: 1

entryprices = []

today = date.today()
today = today.strftime("%Y-%m-%d")

if df["Entry Price"].isna().sum().sum() != 0:
    tickers = df["Pitch"].tolist()
    dates = df["Date of Next Open"].tolist()
    for i in range(0,len(tickers)):
        data = yf.download(tickers[i],start="2023-01-01",end=today)
        entryprice = round(data.loc[dates[i]]["Open"],2)
        entryprices.append(entryprice)
    df["Entry Price"] = entryprices
    df.to_csv('IBOARD.csv')


counts = df[df['Winner?'] == 'Yes']['Team'].value_counts()

# Create a dataframe with the counts and rank the teams
df_counts = pd.DataFrame({'team': counts.index, 'count': counts.values})
df_counts['rank'] = df_counts['count'].rank(method='dense', ascending=False)

# Select the top four teams
top_teams = df_counts[df_counts['rank'] <= 4]['team'].tolist()
# Count the total number of wins for each team


# Assign each team to a different variable
first_place = top_teams[0]
second_place = top_teams[1]
third_place = top_teams[2]
#ourth_place = top_teams[3]
def count_wins(df, team):
    wins = 0
    for index, row in df.iterrows():
        if row["Winner?"] == "Yes" and row["Team"] == team:
            wins += 1
    return wins
SecondWins = count_wins(df, second_place)
FirstWins = count_wins(df, first_place)
ThirdWins = count_wins(df, third_place)
#FourthWins = count_wins(df, fourth_place)
st.header(f'1. {first_place}: {FirstWins} wins')
st.subheader(f'2. {second_place}: {SecondWins} win')
st.subheader(f'3. {third_place}: {ThirdWins} wins')
st.subheader(f'4. Theta: 0 wins')
st.header("")
st.subheader("Full Data")
AgGrid(df, height=275,fit_columns_on_grid_load=True,theme='dark')

def getprice(ticker,date_str):
    date = datetime.strptime(date_str, "%m/%d/%Y")

    # Download the stock data for the specified date
    data = si.get_data(ticker, start_date=date)
    x = data['open'][0]
    x = round(x, 2)
    return x
def liveprice(ticker):
    current_price = si.get_live_price(ticker)
    current_price = round(current_price,2)
    #round(current_price,5)
    return current_price

st.subheader("Stocks Pitched at I-Board:")

#read CSV and list P/L and Buy and Sell values of stocks that won
with open("IBOARD.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    gamma = st.button('Gamma')
    vega = st.button('Vega')
    theta = st.button('Theta')
    delta = st.button('Delta')
    for line in csv_reader:

        #if "Yes" in line:
            if gamma:
                if "Gamma" in line:
                    purchaseprice = float(line[5])
                    currentprice = liveprice(line[2])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)
                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    if change < 0:
                        deltaformat = "-$"
                    else:
                        deltaformat = "$"
                    st.metric(label="Change", value=f'{change}%', delta= (deltaformat + str(total)), delta_color= "normal")
            elif vega:
                if "Vega" in line:
                    purchaseprice = float(line[5])
                    currentprice = liveprice(line[2])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)
                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    if change < 0:
                        deltaformat = "-$"
                    else:
                        deltaformat = "$"
                    st.metric(label="Change", value=f'{change}%', delta= (deltaformat + str(total)), delta_color= "normal")
            elif theta:
                if "Theta" in line:
                    purchaseprice = float(line[5])
                    currentprice = liveprice(line[2])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)
                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    if change < 0:
                        deltaformat = "-$"
                    else:
                        deltaformat = "$"
                    st.metric(label="Change", value=f'{change}%', delta= (deltaformat + str(total)), delta_color= "normal")
            elif delta:
                if "Delta" in line:
                    purchaseprice = float(line[5])
                    currentprice = liveprice(line[2])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)
                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    if change < 0:
                        deltaformat = "-$"
                    else:
                        deltaformat = "$"
                    st.metric(label="Change", value=f'{change}%', delta= (deltaformat + str(total)), delta_color= "normal")


data = pd.read_csv("IBOARD.csv")
for (team), group in data.groupby(['Team']):
    group.to_csv(f'{team}.csv', index=False)


gamma = pd.read_csv("Gamma.csv")
vega = pd.read_csv("Vega.csv")
theta = pd.read_csv("Theta.csv")
delta = pd.read_csv("Delta.csv")

print(gamma.head())
print()
print(vega.head())
print()
print(theta.head())
print()
print(delta.head())



#print(pd.read_csv("Vega.csv"))
#print(pd.read_csv("Gamma.csv"))
#print(pd.read_csv("Theta.csv"))
#print(pd.read_csv("Delta.csv"))



#with open("IBOARD.csv", "r") as csv_file:
    #csv_reader = csv.reader(csv_file)

    #for line in csv_reader:

    #   if "Yes" in line:
    #       second_word = line[1]
    #       st.button(second_word)
    #       buy = line[4]
    #       sell = line[5]
    #       if buy.isdigit() and sell.isdigit():
    #          pl = int(buy)-int(sell)
    #       st.write("Buy Value: "+buy+"\nSell Value: "+sell)
    #       if pl<0:
    #           unrealized = "("+str(pl)+")"
    #       else:
    #          unrealized = str(pl)
    #       st.write("Unrealized P/L: "+unrealized)

# Print results.

