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

import requests

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

    .st-d8 {
        color: black;
    }
                
    .st-ek {
        color: black;
    } 
</style>""", unsafe_allow_html=True)

# Header and personalized greeting
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Student'

# Personalized welcome message
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Search Alumni</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Fetch the data from the API
response = requests.get("http://web-api:4000/alumni")
data = response.json()

# Convert the response data to a DataFrame
data_table1 = pd.DataFrame(data, columns=["Name", "Major", "Role", "Company"])

# Ensure there's a 'Profile_Picture' column in the imported data
# You can either set default placeholders or leave them empty for now
# Assuming data_table1 has 40 rows and you want to assign Grad_Year

grad_years = ['24', '23', '22', '21']  # Example values
# Repeat the grad_year list to match the length of the DataFrame
data_table1['Grad_Year'] = (grad_years * (len(data_table1) // len(grad_years))) + grad_years[:len(data_table1) % len(grad_years)]
# Sample alumni data based on imported API data
alumni_data = data_table1.copy()

# Create a 3-column layout for filtering options
col1, col2, col3 = st.columns(3)

# Add cascader inputs in each column for filtering
with col1:
    selected_internship = st.multiselect(
        'Field of Work',
        options=alumni_data['Role'].unique(),
        default=[],  # No default selection
        help="Select one or more companies"
    )

with col2:
    selected_field_of_work = st.multiselect(
        'Company',
        options=alumni_data['Company'].unique(),
        default=[],  # No default selection
        help="Select one or more fields of work"
    )

with col3:
    selected_major = st.multiselect(
        'Major',
        options=alumni_data['Major'].unique(),
        default=[],  # No default selection
        help="Select one or more majors"
    )

# Ensure selected values are lists, even if only one item is selected
selected_internship = selected_internship if selected_internship else []
selected_field_of_work = selected_field_of_work if selected_field_of_work else []
selected_major = selected_major if selected_major else []

# Apply filters based on selections
filtered_data = alumni_data.copy()  # Ensure original data is preserved

if selected_internship:  # 'Field of Work' filters 'Role'
    filtered_data = filtered_data[filtered_data['Role'].isin(selected_internship)]
if selected_field_of_work:  # 'Company' filters 'Company'
    filtered_data = filtered_data[filtered_data['Company'].isin(selected_field_of_work)]
if selected_major:  # 'Major' filters 'Major'
    filtered_data = filtered_data[filtered_data['Major'].isin(selected_major)]

# Number of items per page
items_per_page = 10

# Calculate the total number of pages
total_pages = -(-len(filtered_data) // items_per_page)  # Round up division

# Add pagination control
current_page = sac.pagination(
    align='center', 
    jump=True, 
    show_total=True, 
    total=len(filtered_data)
) or 1  # Default to page 1 if no selection

# Calculate the range of data to display
start_idx = (current_page - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_data = filtered_data.iloc[start_idx:end_idx]

# Display the filtered alumni data (only for the current page)
if not paginated_data.empty:
    st.markdown(f'''
        <p style="font-weight: 300; font-size: 15px; "margin-top: 40px; margin-bottom: 5px;">
            Showing page {current_page} of {total_pages} ({len(filtered_data)} alumni found)
        </p>
        <hr style="margin-top: 20px; margin-bottom: 20px;">
    ''', unsafe_allow_html=True)
    
    # Custom layout for displaying images and information
    for index, row in paginated_data.iterrows():
        col1, col2, col3, col4 = st.columns([0.9, 2.1, 3, 2])
        with col1:  
             # Default image if no URL is provided
            image_url = row.get('ProfilePic') 
            # Load image with error handling
            try:
                st.image(image_url, width=90)
            except:
                st.image("assets/anonprofilepicred.svg", width=90)  # Fallback image

        with col2:
            st.markdown(f"<p style='margin-top: 11px; margin-bottom: 0px;font-size: 25px; font-weight: 100;'>{row['Name']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='margin-top: 3px; margin-bottom: 5px;font-size: 15px; font-weight: 300;'>{row['Major']} | '{row['Grad_Year']}", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style='margin-top: 20px;'>  
                    <p style='margin-bottom: 5px; font-size: 16px;'>
                        <strong>Field of Work:</strong> {row['Role']}
                    </p>
                    <p style='margin-bottom: 5px; font-size: 16px;'>
                        <strong>Company:</strong> {row['Company']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            if st.button(f"View Profile", key=f"{current_page}_{index}"):
                st.session_state['selected_profile'] = row.to_dict()
                st.switch_page('pages/33_Alumni_Profiles.py')
                
        st.markdown('<hr style="margin-top: 5px; margin-bottom: 20px;">', unsafe_allow_html=True)
