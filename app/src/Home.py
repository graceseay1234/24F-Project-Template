##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################
# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks
try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac
import pandas as pd




m = st.markdown("""
<style>
    /* Link to Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    /* Set font for the whole page */
    body {
        font-family: 'Open Sans', sans-serif;
        margin-bottom: -10px;  /* Reduce the space below "Welcome to" */
    }   

    .light-text {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300;  /* light */
        margin-top: 10px;
    }

    /* Optional: Adjust the font size for titles */
    h1 {
        font-family: 'Open Sans', sans-serif;
        margin-bottom: -30px;  /* Reduce the space below "Welcome to" */
    }

    div.stSelectbox > div > div > div > select {
        font-size: 18px;  /* Increase the font size */
        padding: 20px;    /* Increase the padding for larger select boxes */
        border-radius: 8px;  /* Optional: Make the select box rounded */
        border: 2px solid #ddd;  /* Optional: Change the border color */
    }

    div.stButton > button:first-child {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300; /* light weight */
        font-size: 16px;  
        background-color: rgb(255,255,255);
        color: rgb(0,0,0);
        border: 1px solid rgb(235,235,235);
        border-radius: 8px 8px 8px 8px;
        text-align: left; 
        box-shadow: rgba(211, 211, 211, 0.5) 0px 0px 0px 0.01rem;
    }
            

</style>""", unsafe_allow_html=True)


# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)



# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt.
logger.info("Loading the Home page of the app")
st.markdown('<h1 style="font-size: 50px;font-weight: 300;">Welcome to</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'
st.markdown('<h1 style="font-size: 70px; font-weight: 600;">HuskyNet</h1>', unsafe_allow_html=True)  # Larger font for 'HuskyNet'
st.write('\n\n')
st.markdown('<p class="light-text" style="font-size: 24px;">HI! Please select your role to login.</p>', unsafe_allow_html=True)


# Sample data for positions and names
data = {
    "Position Title": ["Director of Alumni Relations", "System Admin", "Recruiter", "Student"],
    "Name": ["Carson McCullers", "Alice Walker", "Jordan Johnson", "Margaret Mitchell"],
    "Page": ["pages/00_Pol_Strat_Home.py", "pages/10_USAID_Worker_Home.py", 
             "pages/20_Admin_Home.py", "pages/20_Admin_home.py"],
    "Role": ["pol_strat_advisor", "usaid_worker", "administrator", "professor"]
}

# Load data into DataFrame
df = pd.DataFrame(data)

position = st.selectbox("Select Position Title", df["Position Title"].unique())
filtered_names = df[df["Position Title"] == position]["Name"].unique()
name = st.selectbox("Select Your Name", filtered_names)

# Login button logic
if st.button("Login"):
    user_data = df[(df["Position Title"] == position) & (df["Name"] == name)].iloc[0]
    
    # Update session state
    st.session_state['authenticated'] = True
    st.session_state['role'] = user_data["Role"]
    st.session_state['first_name'] = name
    
    # Logging (optional, remove if not using logger)
    # logger.info(f"Logging in as {name}")
    
    # Redirect to the appropriate page
    st.switch_page(user_data["Page"])