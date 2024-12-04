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

# Show appropriate sidebar links for the role of the currently logged in user
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
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Student'

# Personalized welcome message
st.markdown(
    f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>',
    unsafe_allow_html=True
)
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Search Alumni</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Sample alumni data
alumni_data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Internship': ['Google', 'Apple', 'Microsoft', 'Amazon'],
    'Field_of_work': ['Software Engineering', 'Data Science', 'Product Management', 'Marketing'],
    'Major': ['Computer Science', 'Data Science', 'Business', 'Marketing'],
})

# Create a 3-column layout
col1, col2, col3 = st.columns(3)

# Add cascader inputs in each column
with col1:
    selected_internship = sac.cascader(
        items=[sac.CasItem(internship) for internship in alumni_data['Internship'].unique()],
        label='Internship Experience',
        multiple=True,
        search=True,
        clear=True,
        color='#E14B44'
    )

with col2:
    selected_field_of_work = sac.cascader(
        items=[sac.CasItem(field) for field in alumni_data['Field_of_work'].unique()],
        label='Field of Work',
        multiple=True,
        search=True,
        clear=True,
        color='#E14B44'
    )

with col3:
    selected_major = sac.cascader(
        items=[sac.CasItem(major) for major in alumni_data['Major'].unique()],
        label='Major',
        multiple=True,
        search=True,
        clear=True,
        color='#E14B44'
    )

# Ensure selected values are lists, even if only one item is selected
selected_internship = selected_internship if selected_internship else []
selected_field_of_work = selected_field_of_work if selected_field_of_work else []
selected_major = selected_major if selected_major else []

# Default display is all profiles
filtered_data = alumni_data

# Apply filters only if the user makes selections
if selected_internship:
    filtered_data = filtered_data[filtered_data['Internship'].isin(selected_internship)]

if selected_field_of_work:
    filtered_data = filtered_data[filtered_data['Field_of_work'].isin(selected_field_of_work)]

if selected_major:
    filtered_data = filtered_data[filtered_data['Major'].isin(selected_major)]

# Display the filtered alumni data
st.subheader("Filtered Alumni Profiles")
if not filtered_data.empty:
    st.write(f"Found {len(filtered_data)} alumni matching your criteria:")
    st.write(filtered_data[['Name', 'Internship', 'Field_of_work', 'Major']])
else:
    st.write("No alumni found matching your criteria.")