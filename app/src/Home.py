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
        border-left: 1px solid rgb(0,0,0);
        border-radius: 0px 8px 8px 0px;
        text-align: left; 
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


# Create individual selectboxes for each role with names.
role_pol_strat_advisor = st.selectbox("", ["Director of Alumni Relations", "Carson McCullers"])
role_usaid_worker = st.selectbox("", ["System Admin", "Alice Walker"])
role_admin = st.selectbox("", ["Recruiter", "Jordan Johnson"])
role_professor = st.selectbox("", ["Student", "Margaret Mitchell"])

# Handle the redirection based on the selected role
if role_pol_strat_advisor != "Director of Alumni Relations":
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'pol_strat_advisor'
    st.session_state['first_name'] = role_pol_strat_advisor
    logger.info(f"Logging in as {role_pol_strat_advisor}")
    st.switch_page('pages/00_Pol_Strat_Home.py')

elif role_usaid_worker != "System Admin":
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'usaid_worker'
    st.session_state['first_name'] = role_usaid_worker
    logger.info(f"Logging in as {role_usaid_worker}")
    st.switch_page('pages/10_USAID_Worker_Home.py')

elif role_admin != "Recruiter":
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = role_admin
    logger.info(f"Logging in as {role_admin}")
    st.switch_page('pages/20_Admin_Home.py')

elif role_professor != "Student":
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'Professor'
    st.session_state['first_name'] = role_professor
    logger.info(f"Logging in as {role_professor}")
    st.switch_page('pages/20_Admin_home.py')


