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
#from modules.nav import SideBarLinks
try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac
import pandas as pd

try:
    import streamlit_shadcn_ui as ui
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit_shadcn_ui')
    import streamlit_shadcn_ui as ui


st.set_page_config(
    layout="wide",
)

m = st.markdown("""
<style>
    /* Link to Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    /* Set font for the whole page */
    body {
        font-family: 'Open Sans', sans-serif;
        margin-bottom: -10px;  /* Reduce the space below "Welcome to" */
    }   
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

    div.stButton > button:first-child {
        font-family: 'Open Sans', sans-serif;
        font-weight: 300; /* light weight */
        font-size: 15px;  
        background-color: rgb(255,255,255);
        color: rgb(0,0,0);
        border: 1px solid rgb(235,235,235);
        border-radius: 8px 8px 8px 8px;
        text-align: left; 
        box-shadow: rgba(211, 211, 211, 0.5) 0px 0px 0px 0.01rem;
    }

     div.stButton > button:hover {
        background-color: rgb(230,230,230); /* Slightly darker background on hover */
        color: rgb(0,0,0);
    }
                    
    /* Style select box text */
        div[data-baseweb="select"] > div > div {
            font-weight: 400; /* light weight */
            color: #333;  /* Text color */
            background-color: #F4F4F5
        }     
        
</style>""", unsafe_allow_html=True)


# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
#st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
#SideBarLinks(show_home=True)



# ***************************************************
#    The major content of this page
# ***************************************************

col1, col2= st.columns([0.29, 0.57],gap="large")

with col1:
    st.image("assets/newhuskynetlogo@3x.png")
    

with col2:
    # set the title of the page and provide a simple prompt.
    logger.info("Loading the Home page of the app")
    st.markdown('<h1 style="font-size: 50px;font-weight: 300;">Welcome to</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'
    st.markdown('<h1 style="font-size: 70px; font-weight: 600;">HuskyNet</h1>', unsafe_allow_html=True)  # Larger font for 'HuskyNet'
    st.write('\n\n')
    st.markdown('<p class="light-text" style="font-size: 24px;">Hi! Please select your role to login.</p>', unsafe_allow_html=True)



        # Sample data for positions and names
    data = {
        "Position Title": ["Director of Alumni Relations", "System Admin", "Recruiter", "Student"],
        "Name": ["Carson McCullers", "Alice Walker", "Jordan Johnson", "Margaret Mitchell"],
        "Page": ["pages/00_Dir_Alum_Eng_Home.py", "pages/10_System_Admin_Dashboard.py", 
                "pages/20_Recruiter_Home.py", "pages/31_Student_Home.py"],
        "Role": ["Director_of_Alumni_Engagment", "System_Admin", "Recruiter", "Student"]
    }

    # Load data into DataFrame
    df = pd.DataFrame(data)

    # Define tabs
    tabs = ["Director of Alumni Relations", "System Admin", "Recruiter", "Student"]

    # Use ui.tabs to create the tabs
    selected_tab = ui.tabs(options=tabs, default_value="Director of Alumni Relations", className="w-full", key="tabs1")

    # Loop through each tab and display content conditionally
    for i, tab in enumerate(tabs):
        if selected_tab == tab:  # Check if the selected tab is the current tab
            position = tab
            filtered_names = df[df["Position Title"] == position]["Name"].unique()
            name = st.selectbox(f"Select Your Name ({position})", filtered_names, key=position)
        
            # Login button logic
            if st.button(f"Login as {name}"):
                user_data = df[(df["Position Title"] == position) & (df["Name"] == name)].iloc[0]
                
                # Update session state
                st.session_state['authenticated'] = True
                st.session_state['role'] = user_data["Role"]
                st.session_state['first_name'] = name
                
                # Redirect to the appropriate page
                st.switch_page(user_data["Page"])
