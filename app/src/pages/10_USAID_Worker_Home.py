import logging
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# Set wide layout and page configuration
st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Header and personalized greeting
st.title(f"Welcome, System Administrator {st.session_state['first_name']}!")
st.write("### What would you like to do today?")
st.write("Please select an action from the options below:")

# Option buttons with streamlined design and clear labels
col1, col2 = st.columns(2)

with col1:
    if st.button('🔮 Predict Value Based on Regression Model', use_container_width=True):
        st.switch_page('pages/11_Prediction.py')

with col2:
    if st.button('🌐 View the Simple API Demo', use_container_width=True):
        st.switch_page('pages/12_API_Test.py')

with col1:
    if st.button('📊 View Classification Demo', use_container_width=True):
        st.switch_page('pages/13_Classification.py')

# Additional design considerations
st.markdown("""
    ---
    ### System Diagnostics Overview
    As a system administrator, it’s important to monitor system performance and make informed decisions based on real-time diagnostics data.
    Here, you can access different tools to predict outcomes, test APIs, and evaluate classification models.
""")

# Create a time range for 5 months (e.g., from Jan 2024 to May 2024)
time_range = pd.date_range(start="2024-01-01", periods=5, freq="M")

# Start with a baseline of 100
uptime_values = np.ones(len(time_range)) * 100

# Increase fluctuation scale for more noticeable changes (e.g., scale = 40)
uptime_values += np.random.randn(len(time_range)) * 40  # Larger fluctuation

# Clip values to stay within the range of 0-100
uptime_values = np.clip(uptime_values, 0, 100)

# Create DataFrame
uptime_data = pd.DataFrame({
    "Date": time_range,
    "Uptime": uptime_values
})

# Format Date column to display as 'Month Year' (e.g., 'Jan 2024')
uptime_data["Date"] = uptime_data["Date"].dt.strftime('%b %Y')

# Plot with matplotlib for custom x-axis labels
fig, ax = plt.subplots()

# Plot the uptime data
ax.plot(uptime_data["Date"], uptime_data["Uptime"], marker='o')

# Rotate the x-axis labels to be horizontal
ax.set_xticklabels(uptime_data["Date"], rotation=0)

# Labeling and styling
ax.set_xlabel("Month")
ax.set_ylabel("Uptime (%)")
ax.set_title("System Uptime Over Time")

# Set y-axis limits and ticks
ax.set_ylim(0, 100)
ax.set_yticks([0, 25, 50, 75, 100])

# Show the plot
st.pyplot(fig)

# Display system status with simulated data
cpu_usage = np.random.randint(10, 100)
memory_usage = np.random.randint(40, 80)
disk_space = np.random.randint(50, 90)

st.markdown(f"""
    #### System Status:
    - **CPU Usage**: {cpu_usage}%
    - **Memory Usage**: {memory_usage}%
    - **Disk Space**: {disk_space}%
    
    _Keep an eye on these metrics to ensure smooth operations._
""")

# Include log for troubleshooting or system activity (optional)
st.write("### Activity Log")
st.text_area("Logs", "Log output here...", height=200)
