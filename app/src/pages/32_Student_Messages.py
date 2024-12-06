import logging
import pandas as pd
import streamlit as st
import requests
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

# Fetch messages from the Flask API
messages_url = 'http://web-api:4000/message'  # Assuming Flask runs locally
response = requests.get(messages_url)

if response.status_code == 200:
    messages_data = response.json()  # Messages fetched from the backend
else:
    st.error("Failed to fetch messages from the backend.")

# Convert the data to DataFrame for easier display
messages_df = pd.DataFrame(messages_data, columns=['MessageID', 'MessageContent', 'SenderAlumniID', 'ReceiverAlumniID'])

# Display Messages Table
st.dataframe(messages_df)

# View Message Interaction: When a student clicks on a message
message_id = st.selectbox("Select a Message to View", messages_df['MessageID'])

# Fetch the selected message's details
if message_id is not None:
    message_url = f'http://web-api:4000/message/{message_id}'
    message_response = requests.get(message_url)

    if message_response.status_code == 200:
        selected_message = message_response.json()
        st.markdown(f"**From:** {selected_message[0]['SenderAlumniID']}")
        st.markdown(f"**To:** {selected_message[0]['ReceiverAlumniID']}")
        st.markdown(f"**Message:** {selected_message[0]['MessageContent']}")
    
        # Responding to the message
        st.markdown("### Respond to Message")
        response_content = st.text_area("Write your response here:")

        if st.button("Send Response"):
            # In a real application, you would send this response to the backend.
            response_data = {
                'MessageID': message_id,
                'Content': response_content,
                'SenderAlumniID': st.session_state['first_name'],  # Sender can be derived from session state or input
                'ReceiverAlumniID': selected_message[0]['SenderAlumniID']
            }
            # Send the response to the backend (API call to add new message)
            post_response = requests.post(messages_url, json=response_data)

            if post_response.status_code == 201:
                st.success(f"Your response has been sent!")
            else:
                st.error("Failed to send response.")
    
    else:
        st.error("Failed to fetch the selected message.")

# Compose New Message
st.markdown("### Compose New Message")
recipient = st.text_input("Recipient (e.g., Professor A, T.A. C):")
subject = st.text_input("Subject:")
message_content = st.text_area("Message Content:")

if st.button("Send Message"):
    # Send the new message to the backend
    new_message_data = {
        'MessageID': str(pd.to_datetime('now').timestamp()),  # Unique message ID (timestamp as placeholder)
        'Content': message_content,
        'SenderAlumniID': st.session_state['first_name'],  # Sender info
        'ReceiverAlumniID': recipient
    }
    response = requests.post(messages_url, json=new_message_data)
    
    if response.status_code == 201:
        st.success(f"Message sent to {recipient} with subject: {subject}")
    else:
        st.error("Failed to send the message.")
