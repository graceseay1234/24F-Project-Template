import logging
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

import requests

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

# Styling for the page
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

    div.stSelectbox > div > div > div > select {
        font-size: 18px;
        padding: 20px;
        border-radius: 8px;
        border: 2px solid #ddd;
    }

    div.stButton > button:first-child {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300;
        font-size: 16px;  
        background-color: rgba(151, 166, 195, 0.15);
        color: rgb(0,0,0);
        border: 1px solid rgb(235,235,235);
        border-radius: 8px 8px 8px 8px;
        text-align: left;
    }

    /* Custom CSS to change CasItem text color */
    .ant-cascader-menu-item {
        color: black !important;
    }

    .ant-cascader-menu-item:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }

</style>""", unsafe_allow_html=True)

# Header and personalized greeting
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">System Warnings Dashboard</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Replace this URL with the actual URL of your Flask app
API_URL = "http://web-api:4000/administrators/warnings"

# Make a GET request to fetch all warnings
try:
    response = requests.get(API_URL)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Get the data from the response
    warnings_data = response.json()

    if warnings_data:
        # Convert the warnings data into a DataFrame for better formatting
        df = pd.DataFrame(warnings_data)

        # Show all unique reasons in a dropdown menu for filtering
        reasons = df['Reason'].unique().tolist()
        selected_reason = st.selectbox('Select Warning Reason', reasons)

        # Filter the DataFrame based on the selected reason
        filtered_df = df[df['Reason'] == selected_reason]
    
        # Show a summary of filtered results
        st.markdown(f'''
            <p style="font-weight: 300; font-size: 15px; margin-top: 40px; margin-bottom: 5px;">
                Showing {len(filtered_df)} warnings with the selected reason.
            </p>
            <hr style="margin-top: 20px; margin-bottom: 20px;">
        ''', unsafe_allow_html=True)
        # Display the filtered warnings in a box-style layout
        for index, row in filtered_df.iterrows():
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                # Placeholder for the administrator name and warning details
                st.markdown(f"<p style='font-size: 16px; font-weight: 300;'>Warning ID: {row['WarningID']}</p>", unsafe_allow_html=True)

            with col2:
                st.markdown(f"<p style='font-size: 18px; font-weight: bold;'>Reason: {row['Reason']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 16px; font-weight: 300;'>Alumni: {row['AlumniName']}</p>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<p style='font-size: 14px; font-weight: 300;'>Time: {row['TimeStamp']}</p>", unsafe_allow_html=True)
            st.divider()

    else:
        st.write("No warnings found.")
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred: {e}")
