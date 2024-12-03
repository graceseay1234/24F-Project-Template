import logging
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

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

    /* Custom CSS to change CasItem text color */
    .ant-cascader-menu-item {
        color: black !important;
    }

    .ant-cascader-menu-item:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }

</style>""", unsafe_allow_html=True)

# Header and personalized greeting
st.markdown('<p class="light-text" style="font-size: 24px;">Welcome, System Administrator.</p>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Alumni Profiles</h1>', unsafe_allow_html=True)
sac.divider(align='center', color='gray')


# Function to get user input for filtering options
def user_input_features():
    warning_level = st.sidebar.selectbox('Warning Level', ['All', 'High', 'Medium', 'Low'], index=0)
    status = st.sidebar.selectbox('Status', ['All', 'Critical', 'Warning', 'Normal'], index=0)
    service = st.sidebar.selectbox('Service', ['All', 'Database', 'Web Server', 'Application Server', 'Cache'], index=0)
    data = {'warning_level': warning_level, 'status': status, 'service': service}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

st.subheader('Selected Filter Criteria')
st.write(df)

# Sample system warning data with alumni profiles
alumni_data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'service': ['Database', 'Web Server', 'Application Server', 'Cache'],
    'status': ['Critical', 'Warning', 'Normal', 'Critical'],
    'last_checked': ['2024-12-01 12:45:00', '2024-12-01 12:50:00', '2024-12-01 13:00:00', '2024-12-01 13:05:00'],
    'error_message': ['Disk space low', 'High memory usage', '', 'Cache overload'],
    'warning_level': ['High', 'Medium', 'Low', 'High']
})

# Apply filtering based on user input
selected_warning_level = df['warning_level'][0]
selected_status = df['status'][0]
selected_service = df['service'][0]

filtered_data = alumni_data

if selected_warning_level != 'All':
    filtered_data = filtered_data[filtered_data['warning_level'] == selected_warning_level]

if selected_status != 'All':
    filtered_data = filtered_data[filtered_data['status'] == selected_status]

if selected_service != 'All':
    filtered_data = filtered_data[filtered_data['service'] == selected_service]

# Display the filtered alumni data
st.subheader('Filtered Alumni Profiles')
if not filtered_data.empty:
    st.write(f"Found {len(filtered_data)} alumni matching the selected criteria:")
    st.write(filtered_data[['name', 'service', 'status', 'last_checked', 'error_message', 'warning_level']])
else:
    st.write("No alumni found with the selected criteria.")
