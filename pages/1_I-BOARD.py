import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
#from streamlit_vega_lite import vega_lite_component, AltairComponent



st.markdown("# **:green[ I Board Results :tada:]**")

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
st.header(f'1. {first_place}: {FirstWins} win')
st.subheader(f'2. {second_place}: {SecondWins} win')
st.subheader(f'3. Delta: 0 wins')
st.subheader(f'4. Theta: 0 Wins')
st.header("")
st.subheader("Full Data")
AgGrid(df, height=275,fit_columns_on_grid_load=True,theme='dark')
# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.

# Print results.
st.balloons()
