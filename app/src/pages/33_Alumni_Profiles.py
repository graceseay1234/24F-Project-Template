import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

# Sidebar and layout setup
st.set_page_config(layout='wide')
SideBarLinks()

# Profile styling
st.markdown("""
<style>
    .profile-header { font-size: 50px; font-weight: 300; margin-bottom: 20px; }
    .sub-header { font-size: 25px; font-weight: 400; color: #555; }
    .info-section { margin-top: 20px; }
    .profile-pic { border-radius: 50%; height: 150px; width: 150px; margin-bottom: 20px; }
</style>""", unsafe_allow_html=True)

# Initialize session state for selected_profile
if 'selected_profile' not in st.session_state:
    st.session_state['selected_profile'] = None
    
# Check if a profile has been selected
if st.session_state['selected_profile']:
    selected_alumni = st.session_state['selected_profile']

    # Display the selected alumni's profile
    st.image("assets/anonprofilepicred.svg", width=150)  # Default image if not provided
    st.subheader(selected_alumni['Name'])  # Display selected name
    st.write(f"{selected_alumni['Major']} | {selected_alumni['GradYear']}")

    with st.container(border=True):
        if selected_alumni.get('AboutMe'):
            st.write(f"**About Me:** {selected_alumni['AboutMe']}")

    st.divider()

    with st.container(border=True):
        # Education Section (Dynamically populated)
        st.markdown('<h2 class="sub-header">Education</h2>', unsafe_allow_html=True)
        st.write("**Northeastern University**")
        st.write(f"Major: **{selected_alumni['Major']}**")
        st.write(f"Graduation Year: **{selected_alumni['GradYear']}**")
    with st.container(border=True):

        # Work Experience Section
        st.markdown('<h2 class="sub-header">Work Experience</h2>', unsafe_allow_html=True)

        # Fetch alumni work experience from the API
        api_url = "http://web-api:4000/jobs"  # Endpoint for work experience data
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                work_experience_entries = response.json()
                work_experience_for_selected = [
                    entry for entry in work_experience_entries if entry['Name'] == selected_alumni['Name']
                ]

            if work_experience_for_selected:
                # Sort work experience, making current roles appear first
                work_experience_for_selected = sorted(
                    work_experience_for_selected, 
                    key=lambda work: not work['IsCurrent']
                )

                for work in work_experience_for_selected:
                    with st.container(border=True):
                        st.write(f"{work['Company']}")
                        st.write(f"**Role:** {work['Role']}")
                        st.write(f"{work['Startdate']} - {work['EndDate']}")
                        st.write(f"**Status:** {'Current' if work['IsCurrent'] else 'Not Current'}")
            else:
                st.error(f"Failed to fetch work experience data: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")

else:
    # Default dropdown interface when no profile is selected
    api_url = "http://web-api:4000/alumni"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            alumni_data = response.json()

            if alumni_data:
                # Create a dropdown for selecting alumni by name
                alumni_names = [alumni['Name'] for alumni in alumni_data]
                selected_name = st.selectbox("Select an Alumni", alumni_names, key="dropdown")

                # Find the selected alumni's data
                selected_alumni = next((alumni for alumni in alumni_data if alumni['Name'] == selected_name), None)

                if st.button("View Profile"):
                    # Store selected profile in session state and reload the page
                    st.session_state['selected_profile'] = selected_alumni
                    st.experimental_rerun()

            else:
                st.error("No alumni data found.")
        else:
            st.error(f"Failed to fetch alumni data: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
