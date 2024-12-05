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

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
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
</style>""", unsafe_allow_html=True)

# Header and personalized greeting
st.markdown(
    f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>',
    unsafe_allow_html=True
)
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Messages</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Placeholder for Message Data (Can be replaced with real data from a backend or API)
messages_data = {
    'From': ['Alice', 'Bob', 'Charlie', 'David'],
    'Subject': ['Looking for a role', 'Data Analyst Position', 'HR Manager Inquiry', 'Operations Lead Opportunity'],
    'Date': ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04'],
    'Message': [
        'Hi, I am looking for a software engineering role and would love to connect with you.',
        'I am interested in applying for the Data Analyst position you have available.',
        'I have a few questions about the HR Manager role. Can we schedule a time to chat?',
        'I would like to learn more about the Operations Lead position. Can you provide more details?'
    ],
    'Status': ['Unread', 'Read', 'Unread', 'Unread']
}

# Create a DataFrame with the mock messages data
messages_df = pd.DataFrame(messages_data)

# Display Messages Table
st.markdown("### Recent Messages")
st.dataframe(messages_df)

# View Message Interaction: When a recruiter clicks on a message
message_id = st.selectbox("Select a Message to View", messages_df.index)

# Display the selected message's details
if message_id is not None:
    selected_message = messages_df.iloc[message_id]
    st.markdown(f"**From:** {selected_message['From']}")
    st.markdown(f"**Subject:** {selected_message['Subject']}")
    st.markdown(f"**Date:** {selected_message['Date']}")
    st.markdown(f"**Message:** {selected_message['Message']}")
    
    # Responding to the message
    st.markdown("### Respond to Message")
    response = st.text_area("Write your response here:")

    if st.button("Send Response"):
        # In a real application, you would send this response to the backend.
        st.success(f"Your response to {selected_message['From']} has been sent!")
    
    # Change message status to "Read" once it's selected
    messages_df.at[message_id, 'Status'] = 'Read'
    st.dataframe(messages_df)
    
# Optional: Implement features like 'Mark as Read', 'Archive', or 'Delete'
