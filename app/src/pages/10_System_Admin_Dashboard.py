import logging
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from modules.nav import SideBarLinks

try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

logger = logging.getLogger(__name__)

m = st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    body {
        font-family: 'Open Sans', sans-serif;
        margin-bottom: -10px;
    }   
    .light-text {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300;
        margin-top: 10px;
        margin-bottom: 0px;
    }
    h1 {
        font-family: 'Open Sans', sans-serif;
        margin-bottom: 0px;
    }
</style>""", unsafe_allow_html=True)

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.markdown(
    f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>',
    unsafe_allow_html=True
)

st.markdown('<h1 style="font-size: 50px;font-weight: 300;">Administrator Dashboard</h1>', unsafe_allow_html=True)
sac.divider(align='center', color='gray')

def fetch_all_performance_metrics():
    metric_ids = ["1", "2", "3", "4"]  # List of metric_ids (you can modify this based on your needs)
    all_data = []

    for metric_id in metric_ids:
        url = f'http://web-api:4000/administrators/performance-metrics/{metric_id}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Fetched data for MetricID {metric_id}: {data}")  # Log data to verify it's being fetched
            all_data.extend(data)  # Add the data to the list of all_data
        else:
            logger.error(f"Error fetching data for MetricID {metric_id}: {response.status_code}, Response: {response.text}")
            st.error(f"Error fetching data for MetricID {metric_id}: {response.status_code}, Response: {response.text}")
    
    if all_data:
        return pd.DataFrame(all_data)
    else:
        return None

    
# Column 1: Display uptime graph with red line
col1, col2 = st.columns([2, 2])

def plot_red_line_chart(data, x, y, title):
    plt.figure(figsize=(10, 4))
    plt.plot(data[x], data[y], color='red')
    plt.title(title, fontsize=14, color="#888888")
    plt.xlabel('Time')
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Fetch and display performance metrics
performance_metrics_df = fetch_all_performance_metrics()

if performance_metrics_df is not None:
    with col1:
        st.markdown("<h5 style='color: #888888;font-size: 16px; font-weight: 200;'>Uptime (seconds)</h5>", unsafe_allow_html=True)
        plot_red_line_chart(performance_metrics_df, "TimeStamp", "UpTime", "Uptime")

    with col2:
        st.markdown("<h5 style='color: #888888;font-size: 16px; font-weight: 200;'>Response Time (seconds)</h5>", unsafe_allow_html=True)
        plot_red_line_chart(performance_metrics_df, "TimeStamp", "ResponseTime", "Response Time")
    
    # Log DataFrame details
    logger.info(f"Fetched DataFrame with {performance_metrics_df.shape[0]} rows and {performance_metrics_df.shape[1]} columns.")
    logger.info(performance_metrics_df.head())

    # Display data preview
    st.write("### Data Preview", performance_metrics_df.head())

    # Verify required columns
    required_columns = ['TimeStamp', 'ResponseTime', 'UpTime']
    missing_columns = [col for col in required_columns if col not in performance_metrics_df.columns]
    if missing_columns:
        st.error(f"Missing columns: {missing_columns}")
    else:
        # Convert 'TimeStamp' to datetime
        performance_metrics_df['TimeStamp'] = pd.to_datetime(performance_metrics_df['TimeStamp'], errors='coerce')
        if performance_metrics_df['TimeStamp'].isnull().any():
            st.warning("Some 'TimeStamp' values could not be converted to datetime and will be set as NaT.")
        
        # Convert 'ResponseTime' and 'UpTime' to seconds
        try:
            performance_metrics_df['ResponseTime'] = pd.to_timedelta(performance_metrics_df['ResponseTime']).dt.total_seconds()
            performance_metrics_df['UpTime'] = pd.to_timedelta(performance_metrics_df['UpTime']).dt.total_seconds()
        except Exception as e:
            st.error(f"Error converting 'ResponseTime' or 'UpTime': {e}")
        
        # Final DataFrame check
        if performance_metrics_df.empty:
            st.error("DataFrame is empty after processing.")
        else:
            st.success("Data processing completed successfully.")
            st.write(performance_metrics_df)
else:
    st.error("Failed to fetch data from the API. Please check the API endpoint and try again.")

# Plot Response Time with dynamic Y-axis
fig, ax = plt.subplots()
ax.plot(performance_metrics_df['TimeStamp'], performance_metrics_df['ResponseTime'], label='Response Time')

# Adjust Y-axis to fit data range dynamically
ax.set_ylim(performance_metrics_df['ResponseTime'].min() - 1, performance_metrics_df['ResponseTime'].max() + 1)

# Add labels and legend
ax.set_xlabel('Timestamp')
ax.set_ylabel('Response Time (seconds)')
ax.set_title('Performance Metrics Over Time')
ax.legend()

