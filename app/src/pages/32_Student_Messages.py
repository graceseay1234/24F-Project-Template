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

    /* Custom CSS to change CasItem text color */
    .ant-cascader-menu-item {
        color: black !important;
    }

    .ant-cascader-menu-item:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }

</style>""", unsafe_allow_html=True)

# Header and personalized greeting
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Student'

# Personalized welcome message
st.markdown(f'<p class="light-text" style="font-size: 24px;">Welcome, {st.session_state["first_name"]}.</p>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 50px;font-weight: 200;">Messages</h1>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')

# Placeholder for Message Data (Can be replaced with real data from a backend or API)
messages_data = {
    'From': ['Professor A', 'Professor B', 'T.A. C', 'Professor D'],
    'Subject': ['Assignment 1 Update', 'Exam Reminder', 'Course Feedback', 'Final Exam Info'],
    'Date': ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04'],
    'Message': [
        'The deadline for Assignment 1 has been extended by one week.',
        'Reminder: Your exam is on December 5th.',
        'Please provide feedback on the course using the form.',
        'The final exam will take place on December 12th at 10 AM.'
    ],
    'Status': ['Unread', 'Read', 'Unread', 'Unread']
}

# Create a DataFrame with the mock messages data
messages_df = pd.DataFrame(messages_data)

# Display Messages Table
st.dataframe(messages_df)

# View Message Interaction: When a student clicks on a message
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

# Compose New Message
st.markdown("### Compose New Message")
recipient = st.text_input("Recipient (e.g., Professor A, T.A. C):")
subject = st.text_input("Subject:")
message_content = st.text_area("Message Content:")

if st.button("Send Message"):
    # In a real application, you would send this message to the backend.
    st.success(f"Message sent to {recipient} with subject: {subject}")

