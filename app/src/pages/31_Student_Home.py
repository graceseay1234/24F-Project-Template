#STUDENT
import logging
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modules.nav import SideBarLinks
try:
    import streamlit_antd_components as sac
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit-antd-components')
    import streamlit_antd_components as sac

logger = logging.getLogger(__name__)

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Header and personalized greeting
st.markdown('<h1 style="font-size: 50px;font-weight: 300;">Student Dashboard</h1>', unsafe_allow_html=True) 

st.markdown('<p class="light-text" style="font-size: 24px;">Welcome, Student.</p>', unsafe_allow_html=True)

sac.divider(align='center', color='gray')
