import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Streamlit page config
st.set_page_config(page_title="Crypto Sentiment Visualizer", layout="wide")
st.title("📊 Crypto Sentiment Analysis")

# Upload CSV
uploaded_file = st.file_uploader("Upload your sentiment CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert 'Datetime' column to datetime objects
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Date and time input for filtering
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=df['Datetime'].min().date())
        start_time = st.time_input("Start time", value=datetime.now().time())
    with col2:
        end_date = st.date_input("End date", value=df['Datetime'].max().date())
        end_time = st.time_input("End time", value=(datetime.now() + timedelta(hours=1)).time())

    # Combine date and time
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    # Filter DataFrame
    filtered_df = df[(df['Datetime'] >= start_datetime) & (df['Datetime'] <= end_datetime)]

    if filtered_df.empty:
        st.warning("No data found for the selected date and time range.")
    else:
        # Display filtered data
        st.subheader("Filtered Sentiment Data")
        st.dataframe(filtered_df)

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(filtered_df['Datetime'], filtered_df['Sentiment'], label='Sentiment', color='dodgerblue', marker='o')
        ax.set_title("Crypto Sentiment Over Time", fontsize=16)
        ax.set_xlabel("Datetime")
        ax.set_ylabel("Sentiment Score")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
