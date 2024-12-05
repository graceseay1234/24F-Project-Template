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
                            
    .st-ek {
        color: black;
    }          

</style>""", unsafe_allow_html=True)

# Header and personalized greeting
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Alumni Profiles</h1>', unsafe_allow_html=True)
sac.divider(align='center', color='gray')

# Replace this URL with your API's delete endpoint
DELETE_API_URL = "http://web-api:4000/alumni/delete_alumni"

# Fetch the data from the API
response = requests.get("http://web-api:4000/alumni")
data = response.json()

# Convert the response data to a DataFrame
data_table1 = pd.DataFrame(data, columns=["Name", "Major", "Role", "Company"])

# Ensure there's a 'Profile_Picture' column in the imported data
grad_years = ['24', '23', '22', '21']
data_table1['Grad_Year'] = (grad_years * (len(data_table1) // len(grad_years))) + grad_years[:len(data_table1) % len(grad_years)]

# Sample alumni data based on imported API data
alumni_data = data_table1.copy()

# Create a 3-column layout for filtering options
col1, col2, col3 = st.columns(3)

# Add cascader inputs in each column for filtering
with col1:
    selected_internship = st.multiselect('Field of Work', options=alumni_data['Role'].unique(), default=[])
with col2:
    selected_field_of_work = st.multiselect('Company', options=alumni_data['Company'].unique(), default=[])
with col3:
    selected_major = st.multiselect('Major', options=alumni_data['Major'].unique(), default=[])

# Apply filters based on selections
filtered_data = alumni_data.copy()
if selected_internship:  
    filtered_data = filtered_data[filtered_data['Role'].isin(selected_internship)]
if selected_field_of_work:
    filtered_data = filtered_data[filtered_data['Company'].isin(selected_field_of_work)]
if selected_major:
    filtered_data = filtered_data[filtered_data['Major'].isin(selected_major)]

# Number of items per page
items_per_page = 10
total_pages = -(-len(filtered_data) // items_per_page)  # Round up division

# Add pagination control
current_page = sac.pagination(total=total_pages, align='center', jump=True, show_total=True) or 1
start_idx = (current_page - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_data = filtered_data.iloc[start_idx:end_idx]

# Display the filtered alumni data (only for the current page)
if not paginated_data.empty:
    st.markdown(f'''
        <p style="font-weight: 300; font-size: 15px;">Showing page {current_page} of {total_pages} ({len(filtered_data)} alumni found)</p>
        <hr style="margin-top: 20px; margin-bottom: 20px;">
    ''', unsafe_allow_html=True)

for index, row in paginated_data.iterrows():
    col1, col2, col3, col4 = st.columns([0.9, 2.1, 3, 2])
    
    with col1:
        image_url = row.get('ProfilePic')
        try:
            st.image(image_url, width=90)
        except:
            st.image("assets/anonprofilepicred.svg", width=90)

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
        if st.button(f"Delete Profile", key=f"delete_{index}"):
            if pd.notna(row.get('AlumniID')):
                response = requests.delete(f"{DELETE_API_URL}/{row['AlumniID']}")
                if response.status_code == 200:
                    st.success(f"{row['Name']}'s profile has been deleted successfully.")
                    # Log the delete response
                    logging.info(f"Delete response: {response.json()}")
                    # Re-fetch the data after deletion to refresh the table
                    response = requests.get("http://web-api:4000/alumni")
                    if response.status_code == 200:
                        data = response.json()
                        logging.info(f"Fetched data after deletion: {data}")
                        if data:
                            alumni_data = pd.DataFrame(data, columns=["Name", "Major", "Role", "Company"])
                            alumni_data['Grad_Year'] = (grad_years * (len(alumni_data) // len(grad_years))) + grad_years[:len(alumni_data) % len(grad_years)]
                            filtered_data = alumni_data.copy()  # Reset filtered data to the latest data
                            st.write(alumni_data)  # This will display the updated table
                        else:
                            st.warning("No data available to display.")
                    else:
                        st.error("Failed to fetch updated alumni data.")
                else:
                    st.error(f"Failed to delete {row['Name']}'s profile.")
                    logging.error(f"Failed to delete profile: {response.text}")
            else:
                logging.error(f"No 'AlumniID' found for {row['Name']}")
                st.warning(f"{row['Name']} does not have a valid 'AlumniID'. Unable to delete profile.")

    
    st.markdown('<hr style="margin-top: 5px; margin-bottom: 20px;">', unsafe_allow_html=True)


st.write(data)
st.write(data_table1.columns)