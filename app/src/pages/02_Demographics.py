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

st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Demographics</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'

sac.divider(align='center', color='gray')

            # Fetch alumni majors from the Flask API
response = requests.get("http://web-api:4000/majors")
majors = response.json()

# Create a container for the entire "User Demographics" section
with st.container(border=True):
    st.markdown('<p class="light-text" style="font-size: 20px;">Alumni Demographics</p>', unsafe_allow_html=True)


    # Create two columns inside the User Demographics container
    col1, col2 = st.columns([1, 1])  # Equal width columns for majors and locations

    # Custom colors for the pie charts
    custom_colors = ['#FF4B4B', '#FD7D7D', '#FFA0A0', '#FDC5C5']
    # ----------------- Left Column: Major Distribution -----------------
    with col1:
        with st.container(border=True):
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

    # ----------------- Right Column: Location Distribution -----------------
    with col2:
        with st.container(border=True):
            st.markdown("<h5 style='font-size: 15px; font-weight: 300;'>Location Distribution</h5>", unsafe_allow_html=True)
            locations = ['New York', 'California', 'Texas', 'Florida', 'Washington']
            location_counts = np.random.randint(50, 200, size=5)  # Simulated counts

            location_data = pd.DataFrame({
                'Location': locations,
                'Count': location_counts
            })

            # Create and display the pie chart for locations
            fig_location = px.pie(location_data, values='Count', names='Location', color_discrete_sequence=custom_colors)
            st.plotly_chart(fig_location, use_container_width=True)



# Create a container for the entire "User Demographics" section
with st.container(border=True):
    st.markdown('<p class="light-text" style="font-size: 20px;">Student Demographics</p>', unsafe_allow_html=True)


    # Create two columns inside the User Demographics container
    col1, col2 = st.columns([1, 1])  # Equal width columns for majors and locations

    # Custom colors for the pie charts
    custom_colors = ['#FF4B4B', '#FD7D7D', '#FFA0A0', '#FDC5C5']
    # ----------------- Left Column: Major Distribution -----------------
    with col1:
        with st.container(border=True):
            st.markdown("<h5 style='font-size: 15px; font-weight: 300;'>Major Distribution</h5>", unsafe_allow_html=True)
            majors = ['Computer Science', 'Business', 'Psychology', 'Biology', 'Engineering']
            major_counts = np.random.randint(50, 150, size=5)  # Simulated counts

            major_data = pd.DataFrame({
                'Major': majors,
                'Count': major_counts
            })

            # Create and display the pie chart for majors
            fig_major = px.pie(major_data, values='Count', names='Major', color_discrete_sequence=custom_colors)
            st.plotly_chart(fig_major, use_container_width=True)

    # ----------------- Right Column: Location Distribution -----------------
    with col2:
        with st.container(border=True):
            st.markdown("<h5 style='font-size: 15px; font-weight: 300;'>Location Distribution</h5>", unsafe_allow_html=True)
            locations = ['New York', 'California', 'Texas', 'Florida', 'Washington']
            location_counts = np.random.randint(50, 200, size=5)  # Simulated counts

            location_data = pd.DataFrame({
                'Location': locations,
                'Count': location_counts
            })

            # Create and display the pie chart for locations
            fig_location = px.pie(location_data, values='Count', names='Location', color_discrete_sequence=custom_colors)
            st.plotly_chart(fig_location, use_container_width=True)



# Create a container for the entire "User Demographics" section
with st.container(border=True):
    st.markdown('<p class="light-text" style="font-size: 20px;">Recruiter Demographics</p>', unsafe_allow_html=True)


    # Create two columns inside the User Demographics container
    col1, col2 = st.columns([1, 1])  # Equal width columns for majors and locations

    # Custom colors for the pie charts
    custom_colors = ['#FF4B4B', '#FD7D7D', '#FFA0A0', '#FDC5C5']
    # ----------------- Left Column: Major Distribution -----------------
    with col1:
        
        with st.container(border=True):
            st.markdown("<h5 style='font-size: 15px; font-weight: 300;'>Major Distribution</h5>", unsafe_allow_html=True)
            majors = ['Computer Science', 'Business', 'Psychology', 'Biology', 'Engineering']
            major_counts = np.random.randint(50, 150, size=5)  # Simulated counts

            major_data = pd.DataFrame({
                'Major': majors,
                'Count': major_counts
            })

            # Create and display the pie chart for majors
            fig_major = px.pie(major_data, values='Count', names='Major', color_discrete_sequence=custom_colors)
            st.plotly_chart(fig_major, use_container_width=True)

    # ----------------- Right Column: Location Distribution -----------------
    with col2:
        with st.container(border=True):
            st.markdown("<h5 style='font-size: 15px; font-weight: 300;'>Location Distribution</h5>", unsafe_allow_html=True)
            locations = ['New York', 'California', 'Texas', 'Florida', 'Washington']
            location_counts = np.random.randint(50, 200, size=5)  # Simulated counts

            location_data = pd.DataFrame({
                'Location': locations,
                'Count': location_counts
            })

            # Create and display the pie chart for locations
            fig_location = px.pie(location_data, values='Count', names='Location', color_discrete_sequence=custom_colors)
            st.plotly_chart(fig_location, use_container_width=True)


