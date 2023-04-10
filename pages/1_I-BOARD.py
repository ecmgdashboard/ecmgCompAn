import csv
import pandas as pd
import streamlit as st
from datetime import datetime
from yahoo_fin import stock_info as si
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
#from streamlit_vega_lite import vega_lite_component, AltairComponent

st.markdown("# **:green[ I-Board Results :tada:]**")

df = pd.read_csv("IBOARD.csv")


# Output: 1

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
#third_place = top_teams[2]
#ourth_place = top_teams[3]
def count_wins(df, team):
    wins = 0
    for index, row in df.iterrows():
        if row["Winner?"] == "Yes" and row["Team"] == team:
            wins += 1
    return wins
SecondWins = count_wins(df, second_place)
FirstWins = count_wins(df, first_place)
#ThirdWins = count_wins(df, third_place)
#FourthWins = count_wins(df, fourth_place)
st.header(f'1. {first_place}: {FirstWins} wins')
st.subheader(f'2. {second_place}: {SecondWins} win')
st.subheader(f'3. Delta: 0 wins')
st.subheader(f'4. Theta: 0 wins')




def getprice(ticker,date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")

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

teams = ['']+['Gamma'] + ['Vega'] + ['Theta'] + ["Delta"]
st.write("")
st.header('')
st.header('')
st.subheader("Percent Change of Stocks Pitched by Each Team ")
team = st.selectbox("Select A Team Name",teams)

#read CSV and list P/L and Buy and Sell values of stocks that won
with open("IBOARD.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:

        #if "Yes" in line:
            if team == 'Gamma':
                if "Gamma" in line:
                    purchaseprice = getprice(line[1], line[2])
                    currentprice = liveprice(line[1])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)

                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    st.metric(label="Change", value=f'{change}%', delta=f'{total} USD')
            elif team == 'Vega':
                if "Vega" in line:
                    purchaseprice = getprice(line[1], line[2])
                    currentprice = liveprice(line[1])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)

                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    st.metric(label="Change", value=f'{change}%', delta=f'{total} USD')
            elif team == 'Theta':
                if "Theta" in line:
                    purchaseprice = getprice(line[1], line[2])
                    currentprice = liveprice(line[1])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)

                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    st.metric(label="Change", value=f'{change}%', delta=f'{total} USD')
            elif team == 'Delta':
                if "Delta" in line:
                    purchaseprice = getprice(line[1], line[2])
                    currentprice = liveprice(line[1])
                    total = round((currentprice - purchaseprice), 2)
                    change = round(((currentprice - purchaseprice) / purchaseprice) * 100, 2)

                    st.header(line[1])
                    st.write(f'Purchased at {purchaseprice}. Currently at {currentprice}')
                    st.metric(label="Change", value=f'{change}%', delta=f'{total} USD')

st.subheader("Full Data")
st.header("")
AgGrid(df, height=275,fit_columns_on_grid_load=True,theme='dark')

data = pd.read_csv("IBOARD.csv")
for (team), group in data.groupby(['Team']):
    group.to_csv(f'{team}.csv', index=False)


#gamma = pd.read_csv("Gamma.csv")
#vega = pd.read_csv("Vega.csv")
#theta = pd.read_csv("Theta.csv")
#delta = pd.read_csv("Delta.csv")

#print(gamma.head())
#print()
#print(vega.head())
#print()
#print(theta.head())
#print()
#print(delta.head())



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

