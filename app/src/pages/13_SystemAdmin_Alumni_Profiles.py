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

# Fetch the data based on warning filter
filter_warnings = st.selectbox('Filter by Warnings', options=['All', 'With Warnings', 'Without Warnings'], index=0)

# Fetch data from Flask API
response_with_warnings = requests.get("http://web-api:4000/alumni_with_warnings")
response_without_warnings = requests.get("http://web-api:4000/alumni_without_warnings")

# Initialize an empty DataFrame
df_with_warnings = pd.DataFrame()
df_without_warnings = pd.DataFrame()

if response_with_warnings.status_code == 200:
    alumni_with_warnings = response_with_warnings.json()
    df_with_warnings = pd.DataFrame(alumni_with_warnings)

if response_without_warnings.status_code == 200:
    alumni_without_warnings = response_without_warnings.json()
    df_without_warnings = pd.DataFrame(alumni_without_warnings)

# Combine the two DataFrames based on the selected filter
if filter_warnings == 'With Warnings':
    alumni_data = df_with_warnings
elif filter_warnings == 'Without Warnings':
    alumni_data = df_without_warnings
else:
    alumni_data = pd.concat([df_with_warnings, df_without_warnings], ignore_index=True)

# Add pagination for the alumni data
items_per_page = 10
total_pages = -(-len(alumni_data) // items_per_page)  # Round up division

# Add pagination control
current_page = sac.pagination(total=total_pages, align='center', jump=True, show_total=True) or 1
start_idx = (current_page - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_data = alumni_data.iloc[start_idx:end_idx]

# Display the filtered alumni data (only for the current page)
if not paginated_data.empty:
    st.markdown(f'''
        <p style="font-weight: 300; font-size: 15px;">Showing page {current_page} of {total_pages} ({len(alumni_data)} alumni found)</p>
        <hr style="margin-top: 20px; margin-bottom: 20px;">
    ''', unsafe_allow_html=True)

    for index, row in paginated_data.iterrows():
        col1, col2, col3, col4 = st.columns([0.9, 2.1, 3, 2])
        
        with col1:
            image_url = row.get('ProfilePic', "")
            try:
                st.image(image_url if image_url else "assets/anonprofilepicred.svg", width=90)
            except:
                st.image("assets/anonprofilepicred.svg", width=90)

        with col2:
            st.markdown(f"<p style='margin-top: 11px; margin-bottom: 0px;font-size: 25px; font-weight: 100;'>{row['Name']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='margin-top: 3px; margin-bottom: 5px;font-size: 15px; font-weight: 300;'>{row['Major']} | '{row['GradYear']}", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style='margin-top: 20px;'>  
                    <p style='margin-bottom: 5px; font-size: 16px;'>
                        <strong>Field of Work:</strong> {row.get('WorkExperience', 'No work experience')}
                    </p>
                    <p style='margin-bottom: 5px; font-size: 16px;'>
                        <strong>Company:</strong> {row.get('Company', 'No company information')}
                    </p>
                    <p style='margin-bottom: 5px; font-size: 16px; color: red;'>
                        <strong>Warning:</strong> {row.get('WarningReason', 'No warnings')}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            if st.button(f"Delete Profile", key=f"delete_{index}"):
                if pd.notna(row.get('AlumniID')):
                    response = requests.delete(f"{DELETE_API_URL}/{row['AlumniID']}")
                    if response.status_code == 200:
                        st.success(f"{row['Name']}'s profile has been deleted successfully.")
                        # Re-fetch the data after deletion to refresh the table
                        response = requests.get("http://web-api:4000/alumni")
                        alumni_data = pd.DataFrame(response.json(), columns=["AlumniID", "Name", "Major", "Role", "Company", "Warnings"])
                        st.experimental_rerun()  # Trigger a rerun to reflect the changes
                    else:
                        st.error(f"Failed to delete {row['Name']}'s profile.")
                else:
                    logger.error(f"No 'AlumniID' found for {row['Name']}")
                    st.warning(f"{row['Name']}'s profile does not have an Alumni ID.")
else:
    st.warning("No alumni profiles match the filter criteria.")
