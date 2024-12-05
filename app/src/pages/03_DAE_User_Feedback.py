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

st.markdown('<h1 style="font-size: 50px;font-weight: 200;">User Feedback</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'

sac.divider(align='center', color='gray')

# Base URL for the API
BASE_URL = "http://web-api:4000"

# Function to fetch feedback data from API
def fetch_feedback_data():
    try:
        response = requests.get(f"{BASE_URL}/feedback")
        if response.status_code == 200:
            data = response.json()

            columns = ["Content", "TimeStamp"]
            df = pd.DataFrame(data, columns=columns)
            return df
        else:
            st.error("Failed to fetch feedback data.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching feedback data: {e}")
        return pd.DataFrame()



# Function to post new feedback
def add_feedback(content):
    payload = {
        "content": content
    }
    try:
        response = requests.post(f"{BASE_URL}/feedback", json=payload)
        if response.status_code == 200:
            st.success("Successfully added feedback!")
        else:
            st.error(f"Failed to add feedback. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        st.error(f"Error adding feedback: {e}")



# Layout: Two columns: one for filters and form, one for displaying data
col1, col2 = st.columns([1.5, 2])

with col1:
    st.subheader("Add New Feedback")
    feedback_description = st.text_area("Feedback Description")

    if st.button("Submit Feedback"):
        if feedback_description:
            add_feedback(feedback_description)
        else:
            st.error("Please fill in all required fields.")

with col2:
    st.subheader("Existing Feedback")
    # Fetch data
    feedback_df = fetch_feedback_data()

    if not feedback_df.empty:
        st.dataframe(feedback_df)
    else:
        st.info("No feedback available")

