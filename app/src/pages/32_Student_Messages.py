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

# Base URL for the API
BASE_URL = "http://web-api:4000"

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

if 'alumni_id' not in st.session_state:
    st.session_state['alumni_id'] = '14'

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

messages_df["MessageID"] = messages_df["MessageID"].astype(int)
messages_df = messages_df.sort_values(by="MessageID", ascending=False)

# Reset the index before displaying the DataFrame
messages_df = messages_df.reset_index(drop=True)

# Display Messages Table
#st.dataframe(messages_df)


def put_message(message_id, new_content):
    payload = {
        "MessageID": message_id,
        "Content": new_content
    }
    try:
        response = requests.put(f"{BASE_URL}/message", json=payload)
        if response.status_code == 200:
            st.success("Successfully cleared message!")
            st.rerun()
        elif response.status_code == 404:
            st.error("Message ID not found.")
        else:
            st.error(f"Failed to update message. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        st.error(f"Error updating message: {e}")

def delete_message(message_id):
    try:
        response = requests.delete(f"{BASE_URL}/delete_message/{message_id}")
        if response.status_code == 200:
            st.success("Successfully deleted message!")
            st.rerun()
        else:
            st.error(f"Failed to delete message. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        st.error(f"Error deleting message: {e}")

if not messages_df.empty:
    h_col1, h_col2, h_col3, h_col4, h_col5, h_col6 = st.columns([1,5,1,1,1,1])
    h_col1.write("MessageID")
    h_col2.write("Content")
    h_col3.write("Sender AlumniID")
    h_col4.write("Receiver AlumniID")
    h_col5.write("Action")

    our_id = int(st.session_state['alumni_id'])

    for idx, row in messages_df.iterrows():
        rec_id = int(row.get('ReceiverAlumniID'))
        sent_id = int(row.get('SenderAlumniID'))
        if rec_id == our_id or sent_id == our_id:
            col1, col2, col3, col4, col5, col6 = st.columns([1,5,1,1,1,1])
            message_id = row.get('MessageID')
            content = row.get('MessageContent')
            sender_id = row.get('SenderAlumniID')
            rec_id = row.get('ReceiverAlumniID')
            col1.write(message_id)
            col2.write(content)
            col3.write(sender_id)
            col4.write(rec_id)

            # Add a Clear Feedback button for this entry
            clear_button_key = f"clear_{message_id}"
            if col5.button("Clear", key=clear_button_key):
                put_message(message_id, "")

            delete_button_key = f"delete_{message_id}"
            if col6.button("Delete", key=delete_button_key):
                delete_message(message_id)
                # Refresh the data after deletion




# View Message Interaction: When a student clicks on a message
# Ensure ReceiverAlumniID and alumni_id are the same type for comparison
filtered_messages_df = messages_df[
    (messages_df['ReceiverAlumniID'].astype(str) == str(st.session_state['alumni_id'])) |
    (messages_df['SenderAlumniID'].astype(str) == str(st.session_state['alumni_id']))
]


# Display a selectbox with the filtered MessageID values
if not filtered_messages_df.empty:
    message_id = st.selectbox("Select a Message to View", filtered_messages_df['MessageID'])
else:
    st.write("No messages available for the current alumni.")


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
                'Content': response_content,
                'SenderAlumniID': selected_message[0]['SenderAlumniID'], 
                'ReceiverAlumniID': selected_message[0]['ReceiverAlumniID']
            }
            # Send the response to the backend (API call to add new message)
            post_response = requests.post(messages_url, json=response_data)

            if post_response.status_code == 201:
                st.rerun()
                st.success(f"Your response has been sent!")
            else:
                st.error("Failed to send response.")
    
    else:
        st.error("Failed to fetch the selected message.")

# Compose New Message
st.markdown("### Compose New Message")
recipient_id = st.text_input("Recipient ID:")
message_content = st.text_area("Message Content:")

if st.button("Send Message"):
    # Send the new message to the backend
    new_message_data = {
        'Content': message_content,
        'SenderAlumniID': st.session_state['alumni_id'],  # Sender info
        'ReceiverAlumniID': recipient_id
    }
    response = requests.post(messages_url, json=new_message_data)
    
    if response.status_code == 201:
        st.success(f"Message sent to {recipient_id}!")
        st.rerun()
    else:
        st.error("Failed to send the message.")
