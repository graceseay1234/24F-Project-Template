#SYSTEM ADMIN DASHBOARD
import logging
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modules.nav import SideBarLinks
try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

logger = logging.getLogger(__name__)

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Header and personalized greeting
#st.title(f"Welcome, System Administrator {st.session_state['first_name']}!")
st.markdown('<h1 style="font-size: 50px;font-weight: 300;">Administrator Dashboard</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'

# Personalized welcome message
st.markdown(
    f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>',
    unsafe_allow_html=True
)
sac.divider(align='center', color='gray')


#st.write("### What would you like to do today?")
#st.write("Please select an action from the options below:")
# Create two columns for layout
col1, col2 = st.columns([2, 2])

# Simulate uptime data (Hourly data for a 24-hour period)
time_range = pd.date_range(start="2024-12-01 00:00", end="2024-12-01 23:59", freq="H")
uptime_percentage = np.random.uniform(95, 100, size=len(time_range))  # Random uptime data between 95-100%

# Simulate response time data (Random values between 100ms and 500ms)
response_time = np.random.uniform(100, 500, size=len(time_range))  # Random response times in ms

# Create DataFrames for both Uptime and Response Time data
uptime_data = pd.DataFrame({
    "Time": time_range,
    "Uptime (%)": uptime_percentage
})

response_time_data = pd.DataFrame({
    "Time": time_range,
    "Response Time (ms)": response_time
})

# Function to plot a graph with a red line
def plot_red_line_chart(data, x, y, title):
    plt.figure(figsize=(10, 4))
    plt.plot(data[x], data[y], color='red')
    plt.title(title, fontsize=14, color="#888888")
    plt.xlabel('Time')
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

# Column 1: Display uptime graph with red line
with col1:
    # Custom header with smaller and lighter text
    st.markdown("<h5 style='color: #888888;font-size: 16px; font-weight: 200;'>Uptime</h5>", unsafe_allow_html=True)
    plot_red_line_chart(uptime_data, "Time", "Uptime (%)", "Uptime")

# Column 2: Display response time graph with red line
with col2:
    # Custom header for Response Time graph
    st.markdown("<h5 style='color: #888888;font-size: 16px; font-weight: 200;'>Response Time</h5>", unsafe_allow_html=True)
    plot_red_line_chart(response_time_data, "Time", "Response Time (ms)", "Response Time")