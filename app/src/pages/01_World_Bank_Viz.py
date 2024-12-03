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

# Generate random data for the chart (6 values between 0 and 200)
random_data = np.random.randint(0, 200, size=6).tolist()

# Create DataFrame with the generated data
data_df = pd.DataFrame({
    "Active User Count": [random_data]
})

# Display the editable data with an area chart
st.data_editor(
    data_df,
    column_config={
        "Active User Count": st.column_config.AreaChartColumn(
            "Active User Count",
            width="large",
            help="The connection requests over the last 6 months",
        ),
    },
    hide_index=True,
)

# Generate random data for the chart (6 values between 0 and 200)
random_data = np.random.randint(0, 200, size=6).tolist()

# Create DataFrame with the generated data
data_df = pd.DataFrame({
    "Connection Requests Over Time": [random_data]
})

# Display the editable data with an area chart
st.data_editor(
    data_df,
    column_config={
        "Connection Requests Over Time": st.column_config.AreaChartColumn(
            "Connection Requests Over Time",
            width="large",
            help="The connection requests over the last 6 months",
        ),
    },
    hide_index=True,
)
# Get the countries from the world bank data
with st.echo(code_location='above'):
    countries: pd.DataFrame = wb.get_countries()
    st.dataframe(countries)

# Create two columns for layout
col1, col2 = st.columns([1, 1])  # First column for active users and connection requests, second column for demographics

# ----------------- Left Column (Active User Count and Connection Requests) -----------------

# Line graph for Active User Count
with col1:
    with st.container(border=True):
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
    with st.container(border=True):
        st.subheader("Connection Requests Over Time")
        connection_requests = np.random.randint(10, 100, size=30)  # Simulated requests

        fig, ax = plt.subplots()
        ax.plot(days, connection_requests, color='red', marker='x')
        ax.set_title('Connection Requests Over Time')
        ax.set_xlabel('Days')
        ax.set_ylabel('Connection Requests')
        ax.grid(True)
        st.pyplot(fig)

# ----------------- Right Column (Demographics) -----------------

# Custom colors
custom_colors = ['#C63D2F', '#E25E3E', '#FF9B50', '#FFBB5C']
custom_colors_blue = ['#C63D2F', '#E25E3E', '#FF9B50', '#FFBB5C']

# Pie chart for User Demographics - Major
with col2:
     with st.container(border=True):
        st.subheader("User Demographics - Major")
        majors = ['Computer Science', 'Business', 'Psychology', 'Biology', 'Engineering']
        major_counts = np.random.randint(50, 150, size=5)  # Simulated counts of students in each major

        major_data = pd.DataFrame({
        'Major': majors,
        'Count': major_counts
    })

        fig = px.pie(major_data, values='Count', names='Major', title='Major Distribution', color_discrete_sequence=custom_colors)
        st.plotly_chart(fig)

# Pie chart for User Demographics - Location
with col2:
    with st.container(border=True):
     st.subheader("User Demographics - Location")
     locations = ['New York', 'California', 'Texas', 'Florida', 'Washington']
     location_counts = np.random.randint(50, 200, size=5)  # Simulated counts of users in each location
     location_data = pd.DataFrame({
        'Location': locations,
        'Count': location_counts})
     fig = px.pie(location_data, values='Count', names='Location', title='Location Distribution', color_discrete_sequence=custom_colors_blue)
     st.plotly_chart(fig)   

    

# Crosstab of countries for reference
with st.echo(code_location='above'):
    slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
    data_crosstab = pd.crosstab(slim_countries['region'], slim_countries['incomeLevel'], margins=False) 
    st.table(data_crosstab)



with st.container(border=True):
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")
