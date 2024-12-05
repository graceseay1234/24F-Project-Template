## RENAME TO DIR_ALUM_ENG_HOME
## Alumni Engagment Dashboard for Director of Alumni Engagement 


import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import requests


m = st.markdown("""
<style>
                
    /* Link to Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    # div.block-container {padding-top:3rem;}

    /* Set font for the whole page */
    body {
        font-family: 'Open Sans', sans-serif;
        margin-bottom: -10px;  /* Reduce the space below "Welcome to" */
    }   

    .light-text {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300;  /* light */
        margin-top: 10px;
        margin-bottom: 0px;
    }

    /* Optional: Adjust the font size for titles */
    h1 {
        font-family: 'Open Sans', sans-serif;
        margin-bottom: 0px;  /* Reduce the space below "Welcome to" */
    }

    div.stSelectbox > div > div > div > select {
        font-size: 18px;  /* Increase the font size */
        padding: 20px;    /* Increase the padding for larger select boxes */
        border-radius: 8px;  /* Optional: Make the select box rounded */
        border: 2px solid #ddd;  /* Optional: Change the border color */
    }

    div.stButton > button:first-child {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300;
        font-size: 16px;  
        background-color: rgba(151, 166, 195, 0.15);
        border: 1px solid rgb(235,235,235);
        border-radius: 8px 8px 8px 8px;
        text-align: left;
    }
                
    

</style>""", unsafe_allow_html=True)


# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Header and personalized greeting
#st.title(f"Welcome, System Administrator {st.session_state['first_name']}!")
# Personalized welcome message
st.markdown(
    f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>',
    unsafe_allow_html=True
)

st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Engagment Dashboard</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'

sac.divider(align='center', color='gray')

# Create two columns for layout
col1, col2 = st.columns([2, 2])

# Simulate uptime data (Hourly data for a 24-hour period)
time_range = pd.date_range(start="2024-01", end="2024-06", freq="M")
uptime_percentage = np.random.uniform(95, 100, size=len(time_range))  # Random uptime data between 95-100%

# Simulate response time data (Random values between 100ms and 500ms)
response_time = np.random.uniform(100, 500, size=len(time_range))  # Random response times in ms

# Create DataFrames for both Uptime and Response Time data
uptime_data = pd.DataFrame({
    "Month": time_range,
    "Active User Count": uptime_percentage
})

response_time_data = pd.DataFrame({
    "Month": time_range,
    "Connection Requests": response_time
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
    st.markdown("<h5 style='color: #888888;font-size: 16px; font-weight: 200;'>Active User Count</h5>", unsafe_allow_html=True)
    plot_red_line_chart(uptime_data, "Month", "Active User Count", "Active User Count")

# Column 2: Display response time graph with red line
with col2:
    # Custom header for Response Time graph
    st.markdown("<h5 style='color: #888888;font-size: 16px; font-weight: 200;'>Connection Requests over Last 6 Months</h5>", unsafe_allow_html=True)
    plot_red_line_chart(response_time_data, "Month", "Connection Requests", "Connection Requests over Last 6 Months")









# Create a container for the entire "User Demographics" section
with st.container(border=True):
    st.markdown('<p class="light-text" style="font-size: 20px;">User Demographics</p>', unsafe_allow_html=True)
    # Create two columns inside the User Demographics container
    col1, col2 = st.columns([4, 1])  # Equal width columns for majors and locations

    # Custom colors for the pie charts
    custom_colors = ['#FF4B4B', '#FD7D7D', '#FFA0A0', '#FDC5C5']
    # ----------------- Left Column: Major Distribution -----------------
    with col1:
       
                        # Fetch alumni majors from the Flask API
            response = requests.get("http://web-api:4000/majors")
            majors = response.json()

            # Count the occurrences of each major
            major_counts = pd.Series([major['Major'] for major in majors]).value_counts()

            # Create a DataFrame for the pie chart
            major_data = pd.DataFrame({
                'Major': major_counts.index,
                'Count': major_counts.values
            })

            # Custom colors for the pie chart
            custom_colors = ['#FF4B4B', '#FD7D7D', '#FFA0A0', '#FDC5C5']

            # ----------------- Left Column: Major Distribution -----------------
            with st.container():
                st.markdown("<h5 style='font-size: 15px; font-weight: 300;'>Major Distribution</h5>", unsafe_allow_html=True)

                # Create and display the pie chart for majors
                fig_major = px.pie(major_data, values='Count', names='Major', color_discrete_sequence=custom_colors)
                st.plotly_chart(fig_major, use_container_width=True)

    with col2:
        if st.button("See More"):
            st.switch_page("pages/02_Demographics.py")
