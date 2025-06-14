import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from utils.backtest_engine import run_backtest
from utils.sheets_logger import log_to_google_sheets
import json
import os

# Load settings
SETTINGS_PATH = os.path.join("config", "settings.json")
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

st.set_page_config(page_title="SP500 AI Trading Bot", layout="wide")
st.title("📊 SP500 AI Day Trading Backtester")

# Sidebar filters
st.sidebar.header("Strategy Filters")
filters = settings["filters"]

for key in filters:
    filters[key] = st.sidebar.checkbox(key, value=filters[key])

starting_capital = st.sidebar.number_input("Starting Capital ($)", min_value=1000, value=settings["starting_capital"])
risk_per_trade = st.sidebar.slider("Risk Per Trade (%)", min_value=0.1, max_value=5.0, value=settings["risk_per_trade_percent"])
multi_tp = st.sidebar.checkbox("Enable Multi-Take Profit", value=settings["multi_tp"])
news_filter = st.sidebar.checkbox("Enable News Filter", value=settings["news_filter"])

asset = st.sidebar.selectbox("Select Asset", options=["SPX", "EURUSD", "GOLD"])
data_path = f"data/{asset}.csv"

# Run Backtest
if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        df, trades, summary = run_backtest(
            data_path,
            filters,
            starting_capital,
            risk_per_trade,
            multi_tp,
            news_filter
        )

        # Plot equity curve
        st.subheader("Equity Curve")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Equity"], mode="lines", name="Equity"))
        st.plotly_chart(fig, use_container_width=True)

        # Summary stats
        st.subheader("Backtest Summary")
        st.metric("Total P&L ($)", f"{summary['total_pnl']:.2f}")
        st.metric("Win Rate (%)", f"{summary['win_rate']:.2f}")
        st.metric("Trades Taken", summary['total_trades'])

        # Show trades table
        st.subheader("Trade Log")
        st.dataframe(trades)

        # Option to export to Google Sheets
        if st.button("Log to Google Sheets"):
            log_to_google_sheets(trades, summary, asset)
            st.success("Logged to Google Sheets ✅")
