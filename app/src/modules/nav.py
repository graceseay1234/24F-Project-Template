# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon=":material/home:")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About HuskyNet", icon=":material/info:")


#### ------------------------ Director of Alumni Engagement ------------------------
def DirAlumEngHomeNav():
    st.sidebar.page_link(
        "pages/00_Dir_Alum_Eng_Home.py", label="Alumni Engagment Dashboard", icon=":material/space_dashboard:"
    )



def DAEFeatureUsageNav():
    st.sidebar.page_link(
        "pages/01_DAE_Feature_Usage.py", label="Feature Usage Overview", icon=":material/feature_search:"
    )

def Demographics():
    st.sidebar.page_link(
        "pages/02_Demographics.py", label="Demographics", icon=":material/pie_chart:"
    )

def DAEUserFeedback():
    st.sidebar.page_link(
        "pages/03_DAE_User_Feedback.py", label="User Feedback", icon=":material/feedback:"
    )

## ------------------------ Role of System Admin ------------------------
# def ApiTestNav():
#     st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon=":material/troubleshoot:")

def AdminDashNav():
    st.sidebar.page_link(
        "pages/10_System_Admin_Home.py", label="System Admin Dashboard", icon=":material/dashboard:"
    )


def SystemWarningsDashboardNav():
    st.sidebar.page_link(
        "pages/11_System_Warnings_Dashboard.py", label="System Warnings", icon=":material/report:"
    )


def SystemAdminAlumniProfilesNavv():
    st.sidebar.page_link(
        "pages/13_SystemAdmin_Alumni_Profiles.py", label="Alumni Profiles", icon=":material/account_box:")
    # st.sidebar.page_link(
    #     "pages/12_API_Test.py", label="test_api", icon=":material/data_table:"
    # )

def AddAlumniPageNav():
    st.sidebar.page_link(
        "pages/14_SystemAdmin_Add_Alumni.py", label="Add Alumni Profile", icon=":material/person_add:"
    )


#### ------------------------ System Recruiter ------------------------
def RecruiterHomeNav():
    st.sidebar.page_link("pages/20_Recruiter_Home.py", label="Hiring Dashboard", icon=":material/space_dashboard:")

def CandidateOverviewNav():   
    st.sidebar.page_link(
        "pages/21_Candidates_Overview.py", label="Candidates Overview", icon=":material/groups:"
    )

def JobsOverviewNav():
    st.sidebar.page_link(
        "pages/22_Jobs_Overview.py", label="Jobs Overview", icon=":material/work:"
    )

def RecruiterMessages():
    st.sidebar.page_link(
        "pages/23_Recruiter_Messages.py", label="Recruiter Messages", icon=":material/mail:"
    )

#### ------------------------ Student Role ------------------------
def StudentPageNav():
    st.sidebar.page_link("pages/31_Student_Home.py", label="Alumni Search", icon=":material/person_search:")


def StudentMessages():
    st.sidebar.page_link("pages/32_Student_Messages.py", label="Student Messages",  icon=":material/mail:")

def AlumniProfilesStudentView():
    st.sidebar.page_link("pages/33_Alumni_Profiles.py", label="Alumni Profile", icon=":material/person:")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/huskynetlogosvg.svg", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show Director of Alum. Eng. Home and DAE Feature Usage if the user is a director of alumni engagement role.
        if st.session_state["role"] == "Director_of_Alumni_Engagment":
            DirAlumEngHomeNav()
            DAEFeatureUsageNav()
            Demographics()
            DAEUserFeedback()

        # If the user role is system admin worker, show the admin dashboard, warning page, and alumni profile page.
        if st.session_state["role"] == "System_Admin":
            AdminDashNav()
            SystemWarningsDashboardNav()
            # ApiTestNav()
            SystemAdminAlumniProfilesNavv()
            AddAlumniPageNav()

        # If the user is a recruiter, give them access to the recruiter home page and candidate page
        if st.session_state["role"] == "Recruiter":
            RecruiterHomeNav()
            CandidateOverviewNav()
            JobsOverviewNav()

        # If the user is an student, give them access to the administrator pages
        if st.session_state["role"] == "Student":
            StudentPageNav()
            StudentMessages()
            AlumniProfilesStudentView()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")


