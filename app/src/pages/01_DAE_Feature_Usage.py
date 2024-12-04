import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()


# Header and personalized greeting
#st.title(f"Welcome, System Administrator {st.session_state['first_name']}!")
st.markdown('<h1 style="font-size: 50px;font-weight: 300;">Feature Usage Overview</h1>', unsafe_allow_html=True)  # Large font for 'Welcome to'

sac.divider(align='center', color='gray')


# # Get the countries from the world bank data
# with st.echo(code_location='above'):
#     countries: pd.DataFrame = wb.get_countries()
#     st.dataframe(countries)

# # Crosstab of countries for reference
# with st.echo(code_location='above'):
#     slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
#     data_crosstab = pd.crosstab(slim_countries['region'], slim_countries['incomeLevel'], margins=False) 
#     st.table(data_crosstab)

# # Container example
# with st.container(border=True):
#     st.write("This is inside the container")
#     st.bar_chart(np.random.randn(50, 3))
# st.write("This is outside the container")


col1, col2 = st.columns([0.7, 0.3]) 


with col1:
    with st.container(border=True):
# ---------------------------
# Most Used Features Section
# ---------------------------
        st.subheader("Most Used Features")

        # Sample data for feature usage
        feature_data = {
            "Feature": ["Login", "Data Export", "Performance Metrics", "User Management", "Reporting"],
            "Usage Count": [1500, 1300, 900, 700, 500]
        }

        df_features = pd.DataFrame(feature_data)

        # Plot bar chart
        fig = px.bar(df_features, x='Feature', y='Usage Count',
    
                    labels={'Feature': 'Feature', 'Usage Count': 'Number of Uses'},
                    color='Usage Count',
                    color_continuous_scale='Blues')

        st.plotly_chart(fig)

with col2: 
    with st.container(border=True):
        # ---------------------------
        # Download Report Section
        # ---------------------------
        st.subheader("Download Reports")

        # Buttons to download reports
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(label="Download Feature Report",
                            data="Sample feature report content here...",
                            file_name="feature_report.pdf",
                            mime="application/pdf")

        with col2:
            st.download_button(label="Download Performance Metrics",
                            data="Sample performance metrics content here...",
                            file_name="performance_metrics.pdf",
                            mime="application/pdf")


col1, col2 = st.columns([0.9, 0.1]) 


with col1:
    with st.container(border=True):
        # ---------------------------
        # Performance Metrics Section
        # ---------------------------
        st.subheader("Performance Metrics")

        # Sample performance data
        performance_data = {
            "Metric": ["Response Time (ms)", "Error Rate (%)", "User Satisfaction (%)"],
            "Value": [120, 0.5, 85]
        }

        df_performance = pd.DataFrame(performance_data)

        # Display metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric(label=df_performance.iloc[0]['Metric'], value=df_performance.iloc[0]['Value'])
        col2.metric(label=df_performance.iloc[1]['Metric'], value=df_performance.iloc[1]['Value'])
        col3.metric(label=df_performance.iloc[2]['Metric'], value=df_performance.iloc[2]['Value'])

        # Optional: Detailed performance plot
        st.write("\n")  # Add spacing
        st.line_chart(np.random.randn(20, 3))  # Replace with real data when available

# Load feedback data (assuming it's stored in 'user_feedback.csv')
@st.cache_data  # Cache data to improve performance
def load_feedback():
    try:
        feedback_df = pd.read_csv("user_feedback.csv")
        return feedback_df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Feedback", "Rating"])

feedback_df = load_feedback()

# Display feedback data if available
if feedback_df.empty:
    st.warning("No feedback data available.")
else:
    # Show the feedback table
    st.subheader("All User Feedback")
    st.dataframe(feedback_df, use_container_width=True)
    
    # Filter feedback by rating
    st.subheader("Filter Feedback by Rating")
    rating_filter = st.slider("Select rating range", 1, 5, (1, 5))
    filtered_feedback = feedback_df[
        (feedback_df["Rating"] >= rating_filter[0]) & 
        (feedback_df["Rating"] <= rating_filter[1])
    ]
    st.dataframe(filtered_feedback, use_container_width=True)

    # Display overall metrics
    st.subheader("Feedback Summary")
    average_rating = feedback_df["Rating"].mean()
    st.write(f"**Average Rating:** {average_rating:.2f} / 5")

    # Download button for exporting feedback
    st.subheader("Download Feedback Report")
    st.download_button(
        label="Download CSV",
        data=feedback_df.to_csv(index=False),
        file_name='user_feedback_report.csv',
        mime='text/csv'
    )


