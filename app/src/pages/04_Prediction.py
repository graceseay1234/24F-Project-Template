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
st.markdown('<p class="light-text" style="font-size: 24px;">Welcome, System Administrator.</p>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">System Warnings Dashboard</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Sample alumni data with warnings
alumni_data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'internship': ['Google', 'Apple', 'Microsoft', 'Amazon'],
    'field_of_work': ['Software Engineering', 'Data Science', 'Product Management', 'Marketing'],
    'major': ['Computer Science', 'Data Science', 'Business', 'Marketing'],
    'warnings': ['Incomplete profile', 'No warnings', 'Missing internship', 'Incomplete profile'],  # New column
})

# Create a layout for the filtering options
col1, col2, col3, col4 = st.columns(4)

# Filter by warnings
with col1:
    selected_warning = sac.cascader(
        items=[sac.CasItem(warning) for warning in alumni_data['warnings'].unique()],
        label='Warning Type',
        index=0,
        multiple=True,
        search=True,
        clear=True,
        color='#E14B44'
    )

# Print selected values for debugging
st.write(f"Selected Warning: {selected_warning}")

# Ensure selected values are lists, even if only one item is selected
selected_warning = selected_warning if isinstance(selected_warning, list) else [selected_warning] if selected_warning else []

# Default display is all profiles
filtered_data = alumni_data

# Filter alumni data based on the selected warnings
if selected_warning:
    filtered_data = alumni_data[
        alumni_data['warnings'].isin(selected_warning)
    ]

# Display the filtered alumni data
if not filtered_data.empty:
    st.write(f"Found {len(filtered_data)} alumni with active warnings:")
    st.write(filtered_data[['name', 'internship', 'field_of_work', 'major', 'warnings']])
else:
    st.write("No alumni found with the selected warning criteria.")
