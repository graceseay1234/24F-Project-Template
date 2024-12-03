import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# Set the header of the page
st.header('Alumni Engagement Overview')

# Access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# Get the countries from the world bank data
with st.echo(code_location='above'):
    countries: pd.DataFrame = wb.get_countries()
    st.dataframe(countries)

# Create two columns for layout
col1, col2 = st.columns([1, 1])  # First column for active users and connection requests, second column for demographics

# ----------------- Left Column (Active User Count and Connection Requests) -----------------

# Line graph for Active User Count
with col1:
    st.subheader("Active User Count Over Time")
    days = np.arange(1, 31)
    active_user_count = np.random.randint(50, 500, size=30)  # Simulated user counts

    fig, ax = plt.subplots()
    ax.plot(days, active_user_count, color='red', marker='o')
    ax.set_title('Active User Count Over Time')
    ax.set_xlabel('Days')
    ax.set_ylabel('Active Users')
    ax.grid(True)
    st.pyplot(fig)

# Line graph for Connection Requests
with col1:
    st.subheader("Connection Requests Over Time")
    connection_requests = np.random.randint(10, 100, size=30)  # Simulated requests

    fig, ax = plt.subplots()
    ax.plot(days, connection_requests, color='blue', marker='x')
    ax.set_title('Connection Requests Over Time')
    ax.set_xlabel('Days')
    ax.set_ylabel('Connection Requests')
    ax.grid(True)
    st.pyplot(fig)

# ----------------- Right Column (Demographics) -----------------

# Pie chart for User Demographics - Major
with col2:
    st.subheader("User Demographics - Major")
    majors = ['Computer Science', 'Business', 'Psychology', 'Biology', 'Engineering']
    major_counts = np.random.randint(50, 150, size=5)  # Simulated counts of students in each major

    major_data = pd.DataFrame({
        'Major': majors,
        'Count': major_counts
    })

    fig = px.pie(major_data, values='Count', names='Major', title='Major Distribution')
    st.plotly_chart(fig)

# Pie chart for User Demographics - Location
with col2:
    st.subheader("User Demographics - Location")
    locations = ['New York', 'California', 'Texas', 'Florida', 'Washington']
    location_counts = np.random.randint(50, 200, size=5)  # Simulated counts of users in each location

    location_data = pd.DataFrame({
        'Location': locations,
        'Count': location_counts
    })

    fig = px.pie(location_data, values='Count', names='Location', title='Location Distribution')
    st.plotly_chart(fig)

# Crosstab of countries for reference
with st.echo(code_location='above'):
    slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
    data_crosstab = pd.crosstab(slim_countries['region'], slim_countries['incomeLevel'], margins=False) 
    st.table(data_crosstab)
