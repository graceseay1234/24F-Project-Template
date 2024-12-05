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

# Fetch alumni data from the Flask API
api_url = "http://web-api:4000/alumni"  # Replace with your Flask API URL
try:
    response = requests.get(api_url)
    if response.status_code == 200:
        alumni_data = response.json()

        if alumni_data:
            # Create a dropdown for selecting alumni by name
            alumni_names = [alumni['Name'] for alumni in alumni_data]
            selected_name = st.selectbox("Select an Alumni", alumni_names)

            # Find the selected alumni's data
            selected_alumni = next((alumni for alumni in alumni_data if alumni['Name'] == selected_name), None)

            if selected_alumni:
                # Display selected alumni's profile
                st.image("assets/anonprofilepicred.svg", width=150)  # Replace with dynamic data or URL
                st.subheader(selected_alumni['Name'])  # Display selected name
                st.write(f"{selected_alumni['Role']} at {selected_alumni['Company']} | {selected_alumni['Major']}")

                st.divider()

                # Education Section (Assuming it could be fetched similarly)
                st.markdown('<h2 class="sub-header">Education</h2>', unsafe_allow_html=True)
                st.write("""
                - **Northeastern University**  
                  B.Sc. in Computer Science, 2014 - 2018  
                """)

                # Career Section (Dynamic Career Experience)
                st.markdown('<h2 class="sub-header">Career Experience</h2>', unsafe_allow_html=True)
                career_data = pd.DataFrame({
                    'Role': ['Data Scientist', 'Research Assistant'],  # Dynamic roles can be added here
                    'Company': ['ABC Corp', 'Northeastern Research Lab'],  # Add dynamic data
                    'Years': ['2018 - Present', '2017 - 2018']  # Add dynamic data
                })
                st.table(career_data)

                # Skills Section (Dynamic Skills)
                st.markdown('<h2 class="sub-header">Skills & Expertise</h2>', unsafe_allow_html=True)
                skills = ["Python", "Machine Learning", "Data Visualization", "SQL"]  # You can populate this dynamically
                st.write(", ".join(skills))

            else:
                st.error("Selected alumni profile not found.")
        else:
            st.error("No alumni data found.")
    else:
        st.error(f"Failed to fetch alumni data: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {e}")
