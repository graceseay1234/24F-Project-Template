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
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Alumni Profiles</h1>', unsafe_allow_html=True)
sac.divider(align='center', color='gray')


# Replace this URL with your API's delete endpoint
DELETE_API_URL = "http://web-api:4000/alumni/delete" 


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
        default=[],  # No default selection\
        help="Select one or more company"
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
    total=total_pages,  # Total number of pages
    align='center',
    jump=True,
    show_total=True
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
    
# Custom layout with delete functionality
for index, row in paginated_data.iterrows():
    col1, col2, col3, col4, col5 = st.columns([0.9, 2.1, 3, 2, 1.5])
    with col1:
        st.image("assets/anonprofilepicred.svg", width=90)
    with col2:
        st.markdown(f"<p style='margin-top: 11px; font-size: 25px;'>{row['Name']}</p>", unsafe_allow_html=True)
        st.write(f"<p style='font-size: 15px;'>{row['Major']} | '{row['Grad_Year']}</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<p style='margin-top: 20px; font-size: 16px;'><strong>Field of Work:</strong> {row['Role']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'><strong>Company:</strong> {row['Company']}</p>", unsafe_allow_html=True)
    
    
    # Delete profile button
    with col5:
        if st.button(f"Delete", key=f"delete_{current_page}_{index}"):
            response = requests.delete(f"{DELETE_API_URL}/{row['id']}")  # Assuming each profile has a unique 'id'
            if response.status_code == 200:
                st.success(f"{row['Name']}'s profile deleted successfully!")
                # Refresh the data after deletion
                st.experimental_rerun()
            else:
                st.error("Failed to delete profile. Please try again.")

    st.markdown('<hr style="margin-top: 5px; margin-bottom: 20px;">', unsafe_allow_html=True)

st.markdown('<hr style="margin-top: 5px; margin-bottom: 20px;">', unsafe_allow_html=True)
