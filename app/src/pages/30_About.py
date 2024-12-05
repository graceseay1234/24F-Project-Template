import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

SideBarLinks()

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    body {
        font-family: 'Open Sans', sans-serif;
    }
    
    .content-text {
        font-family: 'Open Sans', sans-serif;
        font-size: 16px;
    }

    .highlight {
        background-color: #E14B44;
        color: white;
        padding: 4px 8px;
        border-radius: 5px;
    }
</style>""", unsafe_allow_html=True)

# Page title
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">About HuskyNet</h1>', unsafe_allow_html=True)

# Introduction
st.markdown("""
    <p class='content-text'>
        Welcome to <strong>HuskyNet</strong> — the dedicated networking platform designed exclusively for Northeastern University students and alumni. 
        Unlike generic networking sites, HuskyNet leverages data-driven insights to create meaningful connections tailored to your unique academic and professional journey.
    </p>
""", unsafe_allow_html=True)

# Why HuskyNet?
st.markdown('<h1 style="font-size: 30px;font-weight: 200;">Why HuskyNet?</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'

# Tabs for different user types
tab = sac.tabs([
    sac.TabsItem(label='Students'),
    sac.TabsItem(label='Recruiters'),
    sac.TabsItem(label='Universities'),
], align='center', size='lg', color='#E14B44', use_container_width=True)


# Conditional content based on the selected tab
if tab == 'Students':
    st.markdown("""
    <p class='content-text'>
        Traditional networking platforms can feel overwhelming and often lack the precise tools needed to filter connections that truly matter. 
        HuskyNet bridges this gap by offering targeted networking opportunities through powerful filters based on:
    </p>
    """, unsafe_allow_html=True)
    st.markdown("""
        :red-background[**Field of Work:**] Find connections in your specific industry or desired career field.<br>
        <br>
        :red-background[**Major:**] Connect with alumni who share your academic background.<br>
        <br>
        :red-background[**Internship Experience:**] Identify individuals with relevant internship experiences to gain valuable insights.
    """, unsafe_allow_html=True)

elif tab == 'Recruiters':
    st.markdown("""
    <p class='content-text'>
        As an alumnus, HuskyNet empowers you to give back to the Northeastern community by sharing your experiences, offering mentorship, and connecting with students and fellow alumni who share your professional interests. 
        The platform's targeted search features ensure that your expertise reaches those who can benefit most from your insights and guidance.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("""
        :red-background[**Targeted Search:**] Discover talented students and alumni in specific fields.<br>
        <br>
        :red-background[**Event Promotion:**] Highlight recruitment events directly to the Northeastern community.<br>
        <br>
        :red-background[**Engagement Analytics:**] Utilize data-driven insights to enhance your recruitment strategies.
    """, unsafe_allow_html=True)

elif tab == 'Universities':
    st.markdown("""
     <p class='content-text'>
        For universities, HuskyNet provides a powerful tool to track alumni engagement, gain insights into career trajectories, and foster mentorship opportunities. 
        With data-driven insights and targeted networking features, HuskyNet helps institutions build stronger connections within their alumni networks, supporting both students and graduates as they navigate their professional journeys.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("""
        :red-background[**Alumni Tracking:**] Monitor and engage with alumni more effectively.<br>
        <br>
        :red-background[**Data Insights:**] Gain valuable analytics on student career paths and outcomes.<br>
        <br>
        :red-background[**Mentorship Programs:**] Facilitate structured mentoring relationships within your community.
    """, unsafe_allow_html=True)
