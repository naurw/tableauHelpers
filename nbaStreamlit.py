#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 20:50:46 2022

@author: William
"""

#conda install -c conda-forge streamlit
#conda install -c plotly plotly
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time

@st.cache
def loadMe():
    nba_player_feed = pd.read_csv('https://raw.githubusercontent.com/naurw/tableauHelpers/main/nba_player_feed.csv')
    return nba_player_feed

#Load the data:     
nba_player_feed = loadMe()

# =============================================================================
# Title
# =============================================================================

st.title('Overview of NBA 2021-2022 Player Performance')
st.markdown('By: William Ruan')
st.markdown('Last updated: February 26th, 2022')
st.markdown('This dashboard seeks to analyze the seasonal performance of NBA players in who has the highest 3-point average, highest field goal average, most rebounds, and most turnovers.')

#Creating Menu to look at the datasets used in this dashboard
st.markdown('Three national-level datasets were used in this report. To review each dataset, click on the drop down bar below. However, please note that due to the number of observations within these dataset, loading time may take some time. Please give it a moment and take a sip of your favorite drink. :smile:')
selectbar = st.selectbox('Select Dataset', ("NBA 2021-2022"))


def get_dataset(selectbar):
    if selectbar == 'NBA 2021-2022':
        st.write(nba_player_feed)

st.write(get_dataset(selectbar))


