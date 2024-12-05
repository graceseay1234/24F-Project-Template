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

# Initialize logger
logger = logging.getLogger(__name__)

# Show sidebar links for the current user role
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

    .ant-cascader-menu-item {
        color: black !important;
    }

    .ant-cascader-menu-item:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
                            
    .st-ek {
        color: black;
    }          

</style>""", unsafe_allow_html=True)

# Header and personalized greeting
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Add Alumni Profile</h1>', unsafe_allow_html=True)
sac.divider(align='center', color='gray')

# API URL for adding an alumni profile
ADD_ALUMNI_API_URL = "http://web-api:4000/alumni"


name = st.text_input('Name')
major = st.text_input('Major')
grad_year = st.text_input('Graduation Year')
work_experience = st.text_area('Work Experience')
company = st.text_input('Company')
warning_reason = st.text_input('Warning Reason')

# Submit button to add alumni profile
if st.button('Submit Alumni Profile'):
    if not name or not major or not grad_year:
        st.error("Name, Major, and Graduation Year are required fields.")
    else:
        alumni_data = {
            "Name": name,
            "Major": major,
            "GradYear": grad_year,
            "WorkExperience": work_experience,
            "Company": company,
            "WarningReason": warning_reason
        }
        
        # Send POST request to the Flask API
        response = requests.post(ADD_ALUMNI_API_URL, json=alumni_data)

        
    if response.status_code == 200:
        st.success("Alumni profile added successfully!")
    else:
        st.error(f"Failed to add alumni profile. Error: {response.text}")

