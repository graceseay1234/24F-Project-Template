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

# Example Job Data with only Title, Status, and Description
jobs_data = {
    'Job Title': ['Software Engineer', 'Data Analyst', 'HR Manager', 'Marketing Specialist', 'Operations Lead'],
    'Status': ['Open', 'Closed', 'Open', 'In Progress', 'Open'],
    'Description': [
        'Responsible for developing software solutions and collaborating with teams.',
        'Analyzing data to generate insights and help guide decision-making.',
        'Managing human resources functions, including recruitment and employee relations.',
        'Creating and executing marketing strategies to promote products and services.',
        'Overseeing day-to-day operations and ensuring efficiency in business processes.'
    ]
}

# Convert to DataFrame
jobs_df = pd.DataFrame(jobs_data)


col1, col2 = st.columns([0.9, 0.1])

with col1:
    # Display Candidate DataFrame
  st.markdown('<h1 style="font-size: 20px;font-weight: 400;">Jobs Overview</h1>', unsafe_allow_html=True)


# Display Job DataFrame
st.dataframe(jobs_df)
