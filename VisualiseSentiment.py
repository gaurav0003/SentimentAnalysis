import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime

# Set Streamlit page config
st.set_page_config(page_title="Retail Sentiment", layout="wide")

# Load CSV from GitHub
CSV_URL = 'https://raw.githubusercontent.com/gaurav0003/SentimentAnalysis/refs/heads/main/crypto_data.csv'  # 🔁 Replace with your actual GitHub raw CSV URL
df = pd.read_csv(CSV_URL)

# Combine Date and Time into a single datetime column
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y-%m-%d %H:%M:%S')

# Sidebar inputs
st.sidebar.header("Filter by Date")
min_date = df['DateTime'].min().date()
max_date = df['DateTime'].max().date()

start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

# Filter data
filtered_df = df[(df['DateTime'] >= start_datetime) & (df['DateTime'] <= end_datetime)]

if not filtered_df.empty:
    # Extract data
    positive_funding = filtered_df['Positive Funding Rate']
    negative_funding = filtered_df['Negative Funding Rate']
    datetimes = filtered_df['DateTime']
    sessions = filtered_df['Session']

    total_positive = positive_funding.sum()
    total_negative = abs(negative_funding.sum())

    session_colors = {
        'Asia Session (5.30 am)': '#FFF4D2',
        'Asia Session (9.30 am)': '#FFE5AD',
        'UK Session (1.30 pm)': '#D9F8C4',
        'UK Session (5.30 pm)': '#9ADE7B',
        'US Session (9.30 pm)': '#B4D4FF',
        'US Session (1.30 am)': '#8EB8FF'
    }

    # Create layout
    fig, (ax_pie, ax_bar) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1.1, 1.4]})
    fig.patch.set_facecolor('white')
    ax_pie.set_facecolor('white')
    ax_bar.set_facecolor('white')

    fig.suptitle("Retail Market Sentiment Analysis", fontsize=18, fontweight='bold', y=0.98, color='#333333')
    fig.text(0.5, 0.94, f"Data from {start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}",
             ha='center', fontsize=11, color='#555555')

    fig.text(0.5, 0.78, 'Gaurav Invests', fontsize=42, color='gray', alpha=0.08, rotation=25, ha='center', va='center')

    # Pie Chart
    pie_colors = ['#00A9A5', '#B23A48']
    wedges, texts, autotexts = ax_pie.pie([total_positive, total_negative],
                                          labels=['Retailer Bullish', 'Retailer Bearish'],
                                          colors=pie_colors,
                                          autopct='%1.2f%%',
                                          startangle=140,
                                          radius=1.2,
                                          wedgeprops={'edgecolor': 'white', 'linewidth': 1.2},
                                          textprops={'fontsize': 12})
    for text in texts + autotexts:
        text.set_color('#333333')
    ax_pie.set_title('Retailer Sentiment Indicator', fontsize=14, fontweight='bold', color='#444444', pad=10)

    # Bar Chart
    ax_bar.set_ylim(min(negative_funding.min(), 0) * 1.2, positive_funding.max() * 1.2)
    bar_width = 0.8
    index = range(len(datetimes))

    for i, session in enumerate(sessions):
        if session in session_colors:
            ax_bar.add_patch(patches.Rectangle((i - bar_width / 2, ax_bar.get_ylim()[0]),
                                               bar_width,
                                               ax_bar.get_ylim()[1] - ax_bar.get_ylim()[0],
                                               linewidth=0,
                                               color=session_colors[session],
                                               alpha=0.3))

    ax_bar.bar(index, positive_funding, bar_width, label='Retailer Bullish',
               alpha=0.9, color='#00A9A5', edgecolor='white', linewidth=0.8)
    ax_bar.bar(index, negative_funding, bar_width, label='Retailer Bearish',
               alpha=0.9, color='#B23A48', edgecolor='white', linewidth=0.8)

    ax_bar.set_xlabel('Datetime', fontsize=11)
    ax_bar.set_ylabel('Sentiment', fontsize=11)
    ax_bar.set_title('Intra-session Sentiment Breakdown', pad=10, fontsize=13, fontweight='bold', color='#444444')

    tick_step = max(1, len(datetimes) // 10)
    tick_positions = list(range(0, len(datetimes), tick_step))
    tick_labels = [datetimes.iloc[i].strftime('%d %b\n%H:%M') for i in tick_positions]
    ax_bar.set_xticks(tick_positions)
    ax_bar.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=8)
    ax_bar.legend(loc='upper left')

    legend_handles = [patches.Patch(color=color, label=label) for label, color in session_colors.items()]
    fig.legend(handles=legend_handles, loc='upper right', title='Trading Sessions',
               fontsize=9, frameon=True, framealpha=0.95)

    ax_bar.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout(pad=3.0, rect=[0, 0.04, 1, 0.92])

    st.pyplot(fig)

else:
    st.warning("No data available for the selected date range.")
