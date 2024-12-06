import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

st.set_page_config(layout='wide')



# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Styling for the page
m = st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    div.block-container {padding-top:3rem;}
             
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
# Personalized welcome message
st.markdown(
    f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>',
    unsafe_allow_html=True
)

st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Hiring Dashboard</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Layout with columns
col1, col2 = st.columns([0.9, 0.1])

# Candidates Overview Section
with col1:
    response = requests.get("http://web-api:4000/candidate")
    if response.status_code == 200:
        candidates_data = response.json()

        # Check if the response contains data
        if candidates_data:
            # Convert the API response to DataFrame
            candidates_df = pd.DataFrame(candidates_data)
            candidates_df = candidates_df[['CandidateID', 'Name', 'InterviewNotes', 'Qualities', "Status"]]

            # Limit the number of results to 10
            candidates_df = candidates_df.head(10)

            # Display Candidate DataFrame
            st.markdown('<h1 style="font-size: 20px;font-weight: 400;">Candidates Overview</h1>', unsafe_allow_html=True)
            st.dataframe(candidates_df)
        else:
            st.error("No candidates found.")
    else:
        st.error(f"Failed to fetch candidate data from the API. Status Code: {response.status_code}")

with col2: 
    pages = {
        "Candidates Overview": "pages/21_Candidates_Overview.py",  # Match with page name in the .streamlit/pages folder
    }

    switch_page = st.button("See More")
    if switch_page:
        # Switch to the selected page
        page_file = pages["Candidates Overview"]
        st.switch_page(page_file)


# Jobs Overview Section
col1, col2 = st.columns([0.9, 0.1])

with col1:
    st.markdown('<h1 style="font-size: 20px;font-weight: 400;">Jobs Overview</h1>', unsafe_allow_html=True)

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

        # Limit to 10 results
        jobs_df = jobs_df.head(10)

        # Display Job DataFrame
        st.dataframe(jobs_df)

    else:
        st.error(f"Failed to fetch job data. Status code: {response.status_code}")




with col2: 
    pages = {
        "Jobs Overview": "pages/22_Jobs_Overview.py",  # Match with page name in the .streamlit/pages folder
    }

    switch_page = st.button("See More ")
    if switch_page:
        # Switch to the selected page
        page_file = pages["Jobs Overview"]
        st.switch_page(page_file)