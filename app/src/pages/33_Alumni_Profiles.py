import streamlit as st
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

# Profile Header
st.image("assets/anonprofilepicred.svg", width=150)  # Replace with dynamic data or URL

# Personal Details
st.subheader("Alice")  # Replace with dynamic data
st.write("Software Engineer at ABC Corp | Northeastern Alumni, Class of 2018")

st.divider()

# Education Section
st.markdown('<h2 class="sub-header">Education</h2>', unsafe_allow_html=True)
st.write("""
- **Northeastern University**  
  B.Sc. in Computer Science, 2014 - 2018  
""")

# Career Section
st.markdown('<h2 class="sub-header">Career Experience</h2>', unsafe_allow_html=True)
career_data = pd.DataFrame({
    'Role': ['Data Scientist', 'Research Assistant'],
    'Company': ['ABC Corp', 'Northeastern Research Lab'],
    'Years': ['2018 - Present', '2017 - 2018']
})
st.table(career_data)

# Skills Section
st.markdown('<h2 class="sub-header">Skills & Expertise</h2>', unsafe_allow_html=True)
skills = ["Python", "Machine Learning", "Data Visualization", "SQL"]
st.write(", ".join(skills))
