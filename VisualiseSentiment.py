import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime

# Streamlit title
st.set_page_config(layout="wide")
st.title("Retail Market Sentiment Analysis")

# Load the dataset
file_path = 'crypto_data.csv'
df = pd.read_csv(file_path)

# Convert Date and Time columns into a single DateTime column
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y-%m-%d %H:%M:%S')

# Take date input from user using Streamlit widgets
start_datetime = st.datetime_input("Enter Start Datetime", value=datetime(2025, 5, 19, 9, 30))
end_datetime = st.datetime_input("Enter End Datetime", value=datetime(2025, 5, 20, 9, 30))

# Proceed only if user clicks the button
if st.button("Generate Chart"):
    filtered_df = df[(df['DateTime'] >= start_datetime) & (df['DateTime'] <= end_datetime)]

    if not filtered_df.empty:
        # --- All your existing plotting code stays same here ---
        # Just replace plt.show() with st.pyplot(fig)
        
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

        # Set up layout
        fig, (ax_pie, ax_bar) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1.1, 1.4]})
        fig.patch.set_facecolor('white')
        ax_pie.set_facecolor('white')
        ax_bar.set_facecolor('white')

        fig.suptitle("Retail Market Sentiment Analysis", fontsize=18, fontweight='bold', y=0.98, color='#333333')
        fig.text(0.5, 0.94, f"Data from {start_datetime.strftime('%d-%b-%Y')} to {end_datetime.strftime('%d-%b-%Y')}",
                 ha='center', fontsize=11, color='#555555')
        fig.text(0.5, 0.78, 'Gaurav Invests',
                 fontsize=42, color='gray', alpha=0.08,
                 rotation=25, ha='center', va='center')

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

        # Show in Streamlit
        st.pyplot(fig)

    else:
        st.warning("No data available for the specified datetime range.")
