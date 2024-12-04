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

    /* Custom CSS to change CasItem text color */
    .ant-cascader-menu-item {
        color: black !important;
    }

    .ant-cascader-menu-item:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }

</style>""", unsafe_allow_html=True)

# Header and personalized greeting

st.markdown('<h1 style="font-size: 50px;font-weight: 200;">System Warnings Dashboard</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Sample system warning data with categories
system_data = pd.DataFrame({
    'service': ['Database', 'Web Server', 'Application Server', 'Cache'],
    'status': ['Critical', 'Warning', 'Normal', 'Critical'],
    'last_checked': ['2024-12-01 12:45:00', '2024-12-01 12:50:00', '2024-12-01 13:00:00', '2024-12-01 13:05:00'],
    'response_time': ['500ms', '120ms', '40ms', '600ms'],
    'error_message': ['Disk space low', 'High memory usage', '', 'Cache overload'],
    'warning_level': ['High', 'Medium', 'Low', 'High']
})

# Create a layout for the filtering options
col1, col2, col3 = st.columns(3)

# Filter by warning level
with col1:
    selected_warning_level = sac.cascader(
        items=[sac.CasItem(level) for level in system_data['warning_level'].unique()],
        label='Warning Level',
        index=0,
        multiple=True,
        search=True,
        clear=True,
        color='#E14B44'
    )

# Filter by service status
with col2:
    selected_status = sac.cascader(
        items=[sac.CasItem(status) for status in system_data['status'].unique()],
        label='Status',
        index=0,
        multiple=True,
        search=True,
        clear=True,
        color='#E14B44'
    )

# Filter by service type
with col3:
    selected_service = sac.cascader(
        items=[sac.CasItem(service) for service in system_data['service'].unique()],
        label='Service',
        index=0,
        multiple=True,
        search=True,
        clear=True,
        color='#E14B44'
    )


# Ensure selected values are lists, even if only one item is selected
selected_warning_level = selected_warning_level if isinstance(selected_warning_level, list) else [selected_warning_level] if selected_warning_level else []
selected_status = selected_status if isinstance(selected_status, list) else [selected_status] if selected_status else []
selected_service = selected_service if isinstance(selected_service, list) else [selected_service] if selected_service else []

# Default display is all system services
filtered_data = system_data

# Filter system data based on the selected filters
if selected_warning_level:
    filtered_data = filtered_data[filtered_data['warning_level'].isin(selected_warning_level)]

if selected_status:
    filtered_data = filtered_data[filtered_data['status'].isin(selected_status)]

if selected_service:
    filtered_data = filtered_data[filtered_data['service'].isin(selected_service)]

# Display the filtered system data
if not filtered_data.empty:
    st.write(f"Found {len(filtered_data)} system services matching the selected criteria:")
    st.write(filtered_data[['service', 'status', 'last_checked', 'response_time', 'error_message', 'warning_level']])
else:
    st.write("No system services found with the selected criteria.")
