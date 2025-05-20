import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime

st.set_page_config(page_title="Dark Sentiment Dashboard", layout="wide")

# Example CSV source
CSV_URL = 'https://raw.githubusercontent.com/gaurav0003/SentimentAnalysis/refs/heads/main/crypto_data.csv'
df = pd.read_csv(CSV_URL)

df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y-%m-%d %H:%M:%S')

min_date = df['DateTime'].min().date()
max_date = df['DateTime'].max().date()
start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

filtered_df = df[(df['DateTime'] >= start_datetime) & (df['DateTime'] <= end_datetime)]

if not filtered_df.empty:
    positive_funding = filtered_df['Positive Funding Rate']
    negative_funding = filtered_df['Negative Funding Rate']
    datetimes = filtered_df['DateTime']
    sessions = filtered_df['Session']

    total_positive = positive_funding.sum()
    total_negative = abs(negative_funding.sum())

    session_colors = {
        'Asia Session (5.30 am)': '#22272E',
        'Asia Session (9.30 am)': '#2C2F36',
        'UK Session (1.30 pm)': '#1C2D3A',
        'UK Session (5.30 pm)': '#223843',
        'US Session (9.30 pm)': '#263B4A',
        'US Session (1.30 am)': '#1E2B38'
    }

    fig, (ax_pie, ax_bar) = plt.subplots(2, 1, figsize=(13, 10), gridspec_kw={'height_ratios': [1, 1.5]})
    fig.patch.set_facecolor('#0e1117')
    ax_pie.set_facecolor('#0e1117')
    ax_bar.set_facecolor('#0e1117')

    fig.suptitle("📊 Retail Sentiment Analysis (Dark Mode)", fontsize=20, fontweight='bold', color='white', y=0.98)
    fig.text(0.5, 0.93, f"{start_date.strftime('%d-%b-%Y')} ➜ {end_date.strftime('%d-%b-%Y')}",
             ha='center', fontsize=12, color='#bbbbbb')
# Pie Chart
pie_colors = ['#14b887', '#FF4C75']
wedges, texts, autotexts = ax_pie.pie(
    [total_positive, total_negative],
    labels=['Bullish', 'Bearish'],
    colors=pie_colors,
    autopct='%1.1f%%',
    startangle=140,
    radius=1.2,
    wedgeprops={'edgecolor': '#0e1117'},
    textprops={'fontsize': 12, 'color': 'white'}
)

    # Bar Chart
    ax_bar.set_ylim(min(negative_funding.min(), 0) * 1.2, positive_funding.max() * 1.2)
    bar_width = 0.8
    index = range(len(datetimes))

    for i, session in enumerate(sessions):
        if session in session_colors:
            ax_bar.add_patch(patches.Rectangle((i - bar_width / 2, ax_bar.get_ylim()[0]),
                                               bar_width,
                                               ax_bar.get_ylim()[1] - ax_bar.get_ylim()[0],
                                               color=session_colors[session],
                                               alpha=0.3))

    ax_bar.bar(index, positive_funding, bar_width, label='Bullish',
               color='#00FFB3', alpha=0.9, edgecolor='white')
    ax_bar.bar(index, negative_funding, bar_width, label='Bearish',
               color='#FF4C75', alpha=0.9, edgecolor='white')

    ax_bar.set_xlabel("Datetime", color='white')
    ax_bar.set_ylabel("Sentiment Value", color='white')
    ax_bar.set_title("Intra-Session Sentiment", fontsize=14, color='white')

    tick_step = max(1, len(datetimes) // 10)
    tick_positions = list(range(0, len(datetimes), tick_step))
    tick_labels = [datetimes.iloc[i].strftime('%d %b\n%H:%M') for i in tick_positions]
    ax_bar.set_xticks(tick_positions)
    ax_bar.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=8, color='white')
    ax_bar.tick_params(colors='white')
    ax_bar.legend(loc='upper left', facecolor='#1e1e1e', edgecolor='white', fontsize=10)

    fig.legend(handles=[
        patches.Patch(color='#00FFB3', label='Bullish'),
        patches.Patch(color='#FF4C75', label='Bearish')
    ], loc='upper right', fontsize=10, frameon=False)

    ax_bar.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)

    plt.tight_layout(pad=3.0, rect=[0, 0.04, 1, 0.94])
    st.pyplot(fig)
else:
    st.error("No data found for selected range.")
