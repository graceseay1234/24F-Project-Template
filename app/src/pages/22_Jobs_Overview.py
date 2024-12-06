import logging
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
import requests

try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

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
</style>""", unsafe_allow_html=True)

# Header and personalized greeting
st.markdown(
    f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>',
    unsafe_allow_html=True
)
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Jobs Overview</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Fetch jobs data from the Flask API
jobs_url = 'http://web-api:4000/job' 
response = requests.get(jobs_url)

if response.status_code == 200:
    # Assuming the response is a list of jobs, parse it
    jobs_data = response.json()

    # Convert to DataFrame
    jobs_df = pd.DataFrame(jobs_data)

    # Reorder columns so that 'Title' is the first column
    jobs_df = jobs_df[['Title', 'JobID', 'Description', 'Status']]

    col1, col2 = st.columns([0.9, 0.1])

    with col1:
        # Display Job DataFrame
        st.dataframe(jobs_df)

else:
    st.error(f"Failed to fetch job data. Status code: {response.status_code}")
