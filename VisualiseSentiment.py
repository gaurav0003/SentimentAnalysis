import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

# === CONFIG ===
st.set_page_config(page_title="Retail Sentiment Visualizer", layout="wide")

# === TITLE & INFO ===
st.title("🧠 Retail Market Sentiment Analysis")
st.markdown("""
Welcome to the **Retail Market Sentiment Visualizer**!  
This tool helps you analyze bullish and bearish funding sentiment over specific sessions.

👉 **Select a date range** below and hit **Generate Chart** to visualize.
""")

# === DATE INPUTS ===
default_start = datetime.now() - timedelta(days=1)
default_end = datetime.now()

start_datetime = st.datetime_input("📅 Start datetime", value=default_start)
end_datetime = st.datetime_input("📅 End datetime", value=default_end)

# === SAMPLE DATA OPTION ===
if st.checkbox("Use Sample Range"):
    start_datetime = datetime(2024, 9, 1, 5, 30)
    end_datetime = datetime(2024, 9, 2, 5, 30)

# === UPLOAD FUNDING DATA ===
uploaded_file = st.file_uploader("📤 Upload funding data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Time"])
    df = df[(df["Time"] >= start_datetime) & (df["Time"] <= end_datetime)]

    # === GROUP BY TIME ===
    grouped_df = df.groupby("Time").agg({
        "PositiveFR": "sum",
        "NegativeFR": "sum",
        "BTCUSDT": "first",
        "BTCDOMUSDT": "first"
    }).reset_index()

    # === PLOTTING ===
    fig, ax1 = plt.subplots(figsize=(18, 8))

    # Bar chart for FR
    ax1.bar(grouped_df["Time"], grouped_df["PositiveFR"], label="Positive FR", color="green")
    ax1.bar(grouped_df["Time"], -grouped_df["NegativeFR"], label="Negative FR", color="red")
    ax1.set_ylabel("Funding Rate (FR)")
    ax1.set_xlabel("Time")
    ax1.legend(loc="upper left")

    # Line chart for BTCUSDT on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(grouped_df["Time"], grouped_df["BTCUSDT"], color="blue", label="BTCUSDT Price", linewidth=2)
    ax2.set_ylabel("BTC Price", color="blue")
    ax2.tick_params(axis='y', labelcolor='blue')

    # Format x-axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))
    fig.autofmt_xdate()

    # === SESSION BACKGROUND ===
    for i in range(len(grouped_df)):
        session_time = grouped_df["Time"].iloc[i]
        hour = session_time.hour
        if 5 <= hour < 13:
            color, label = "#e0f7fa", "Asia"
        elif 13 <= hour < 21:
            color, label = "#f1f8e9", "UK"
        else:
            color, label = "#fce4ec", "US"
        ax1.axvspan(session_time, session_time + timedelta(hours=1), facecolor=color, alpha=0.3)

    st.pyplot(fig)

else:
    st.warning("📂 Please upload a CSV file to generate the chart.")

# === ERROR HANDLING ===
if start_datetime > end_datetime:
    st.error("❌ Start datetime must be earlier than end datetime.")
