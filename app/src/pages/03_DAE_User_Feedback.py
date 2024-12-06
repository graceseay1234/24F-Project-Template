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

st.markdown('<h1 style="font-size: 50px;font-weight: 200;">User Feedback</h1>', unsafe_allow_html=True) 

sac.divider(align='center', color='gray')

# Base URL for the API
BASE_URL = "http://web-api:4000"

# Function to fetch feedback data from API
def fetch_feedback_data():
    try:
        response = requests.get(f"{BASE_URL}/feedback")
        if response.status_code == 200:
            data = response.json()

            columns = ["FeedbackID", "Content", "TimeStamp"]
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

# Function to edit feedback
def put_feedback(feedback_id, new_content):
    payload = {
        "FeedbackID": feedback_id,
        "Content": new_content
    }
    try:
        response = requests.put(f"{BASE_URL}/feedback", json=payload)
        if response.status_code == 200:
            st.success("Successfully cleared feedback!")
            st.rerun()
        elif response.status_code == 404:
            st.error("Feedback ID not found.")
        else:
            st.error(f"Failed to update feedback. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        st.error(f"Error updating feedback: {e}")


# Function to delete feedback by ID
def delete_feedback(feedback_id):
    try:
        response = requests.delete(f"{BASE_URL}/delete_feedback/{feedback_id}")
        if response.status_code == 200:
            st.success("Successfully deleted feedback!")
            st.rerun()
        else:
            st.error(f"Failed to delete feedback. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        st.error(f"Error deleting feedback: {e}")



st.markdown('<ight-text style="font-size: 25px;font-weight: 400;">Add New Feedback</h1>', unsafe_allow_html=True)
feedback_description = st.text_area("Feedback Description")

if st.button("Submit Feedback"):
    if feedback_description:
        add_feedback(feedback_description)
    else:
        st.error("Please fill in all required fields.")

st.write("---")


st.markdown('<ight-text style="font-size: 25px;font-weight: 400;">Existing Feedback</h1>', unsafe_allow_html=True)
# Fetch data
feedback_df = fetch_feedback_data()
feedback_df["FeedbackID"] = feedback_df["FeedbackID"].astype(int)
feedback_df = feedback_df.sort_values(by="FeedbackID")
if not feedback_df.empty:
    h_col1, h_col2, h_col3, h_col4 = st.columns([1,5,1,1])
    h_col1.write("FeedbackID")
    h_col2.write("Content")
    h_col3.write("Action")

    for idx, row in feedback_df.iterrows():
        col1, col2, col3, col4 = st.columns([1,5,1,1])
        feedback_id = row.get('FeedbackID')
        content = row.get('Content')
        col1.write(feedback_id)
        col2.write(content)

        # Add a Clear Feedback button for this entry
        clear_button_key = f"clear_{feedback_id}"
        if col4.button("Clear", key=clear_button_key):
            put_feedback(feedback_id, "")

        delete_button_key = f"delete_{feedback_id}"
        if col3.button("Delete", key=delete_button_key):
            delete_feedback(feedback_id)
            # Refresh the data after deletion

        
else:
    st.info("No feedback available")

