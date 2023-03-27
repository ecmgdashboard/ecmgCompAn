import streamlit as st
import pandas as pd
st.markdown("# Competitive Analytics")
st.markdown("Update")
def calculate_realized_gains(trades_df):
    """
    Calculates the realized gains as a percentage from a DataFrame of stock trades.

    Args:
        trades_df (pandas.DataFrame): DataFrame containing trades with columns for "Stock",
            "Date", "Price Target", and "Stop Loss".

    Returns:
        float: The total realized gains as a percentage from the trades in the DataFrame.
    """
    total_investment = 0.0
    total_gain = 0.0

    for index, trade in trades_df.iterrows():
        stock_price_data = si.get_data(trade["Stock"], start_date=trade["Date"], end_date=trade["Date"])

        # Check if the stock price hit the price target or stop loss
        if stock_price_data.iloc[0]["high"] >= trade["Price Target"]:
            realized_gain = (trade["Price Target"] - stock_price_data.iloc[0]["open"]) / stock_price_data.iloc[0]["open"]
            total_gain += realized_gain
            total_investment += 1.0
        elif stock_price_data.iloc[0]["low"] <= trade["Stop Loss"]:
            realized_gain = (trade["Stop Loss"] - stock_price_data.iloc[0]["open"]) / stock_price_data.iloc[0]["open"]
            total_gain += realized_gain
            total_investment += 1.0

    if total_investment == 0:
        return 0.0

    realized_gains_pct = (total_gain / total_investment) * 100.0
    return realized_gains_pct
