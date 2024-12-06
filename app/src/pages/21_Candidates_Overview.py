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
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Candidates Overview</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Fetch candidate data from the API
response = requests.get("http://web-api:4000/candidate")
if response.status_code == 200:
    candidates_data = response.json()

    # Check if the response contains data
    if candidates_data:
        # Convert the API response to DataFrame
        candidates_df = pd.DataFrame(candidates_data)
        candidates_df = candidates_df[['CandidateID', 'Name', 'InterviewNotes', 'Qualities', "Status"]]

        # Display Candidate DataFrame
        st.markdown('<h1 style="font-size: 20px;font-weight: 400;">Candidates Overview</h1>', unsafe_allow_html=True)
        st.dataframe(candidates_df)
    else:
        st.error("No candidates found.")
else:
    st.error(f"Failed to fetch candidate data from the API. Status Code: {response.status_code}")

# Add new candidate form
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h1 style="font-size: 20px;font-weight: 400;">Add New Candidate</h1>', unsafe_allow_html=True)

    with st.form(key='add_candidate_form'):
        candidate_id = st.text_input("Candidate ID")  # Only if necessary to manually include it
        name = st.text_input("Candidate Name")
        interview_notes = st.text_area("Interview Notes")
        status = st.selectbox("Status", ["Pending", "Interviewed", "Hired", "Rejected"])
        qualities = st.text_area("Qualities")

        submit_button = st.form_submit_button(label="Add Candidate")

        if submit_button:
            # Prepare candidate data for POST request
            new_candidate = {
                "CandidateID": candidate_id,  # Add this if needed
                "Name": name,
                "InterviewNotes": interview_notes,
                "Status": status,
                "Qualities": qualities
            }

            # Send POST request to Flask API to add the new candidate
            response = requests.post("http://web-api:4000/candidate", json=new_candidate)

            if response.status_code == 201:  # Successfully added
                st.success("New candidate added successfully!")
            else:
                st.error(f"Failed to add candidate. Status Code: {response.status_code}")

# Function to delete a candidate by name
def delete_candidate_by_name(candidate_name):
    try:
        # First, check if any HiringUser records are associated with the candidate
        response = requests.get(f"http://web-api:4000/hiring_user/{candidate_name}")
        if response.status_code == 200:
            hiring_user_data = response.json()
            if hiring_user_data:
                # Delete associated HiringUser records
                st.warning(f"There are dependent records for {candidate_name}. Deleting associated hiring users.")
                delete_response = requests.delete(f"http://web-api:4000/delete_hiring_user/{candidate_name}")
                if delete_response.status_code != 200:
                    st.error(f"Failed to remove hiring user data for {candidate_name}")
                    return
        # Now proceed to delete the candidate
        response = requests.delete(f"http://web-api:4000/delete_candidate_by_name/{candidate_name}")
        if response.status_code == 200:
            st.success(f"Candidate {candidate_name} deleted successfully!")
            st.experimental_rerun()  # Reload the data
        else:
            try:
                error_message = response.json().get('message', 'Unknown error occurred')
                st.error(f"Failed to delete candidate: {error_message}")
            except ValueError:
                st.error(f"Failed to delete candidate: Received non-JSON response.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to delete the candidate: {e}")




# Delete candidate section
with col2:
    response = requests.get("http://web-api:4000/candidate")
    if response.status_code == 200:
        candidates_data = response.json()

        # Display candidate list and delete button
        if candidates_data:
            candidate_names = [candidate['Name'] for candidate in candidates_data]
            
            st.markdown('<h1 style="font-size: 20px;font-weight: 400;">Select a Candidate to Delete</h1>', unsafe_allow_html=True)
            selected_candidate_name = st.selectbox("Candidate Name", candidate_names)

            # Delete button
            if st.button(f"Delete Candidate"):
                delete_candidate_by_name(selected_candidate_name)
        else:
            st.error("No candidates found.")
    else:
        st.error("Failed to fetch candidate data from the API.")
