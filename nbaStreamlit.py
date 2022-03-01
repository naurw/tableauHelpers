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
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/naurw/tableauHelpers/main/nba_player_feed.csv')
    return df

df = load_data()

# =============================================================================
# Title
# =============================================================================

st.title('Overview of NBA Player Performance')
st.markdown('By: William Ruan')
st.markdown('Last updated: February 26th, 2022')
st.markdown('This dashboard seeks to analyze the seasonal performance of NBA players in the following metrics: 3-pointers, field goals, rebounds, and turnovers.')

st.markdown('To review each dataset, click on the drop down bar below. Please give it a moment and take a sip of your favorite drink. :smile:')
selectbar = st.selectbox('Select Dataset', ("NBA 2021-2022"))


def get_dataset(selectbar):
    if selectbar == 'NBA 2021-2022':
        st.write(df)

st.write(get_dataset(selectbar))

# =============================================================================
# Section 1 
# =============================================================================

st.markdown('---')
st.title('NBA Individual Performance')

player_games = df['player'].value_counts().reset_index()
player_games.columns = ['player', 'games_played']
threePts = df[['game_id', 'date', 'player', '3_point', '3_point_attempts']]
twoPts = df[['game_id', 'date', 'player', 'field_goals', 'field_goals_attempts']]
freePts = df[['game_id', 'date', 'player', 'free_throw', 'free_throw_attempts']]
rebound = df[['game_id', 'date', 'player', 'offensive_rebound', 'defensive_rebound', 'total_rebound']]
turnover = df[['game_id', 'date', 'player', 'turnovers']]

pd.options.mode.chained_assignment = None  # default='warn'

player_games = df['player'].value_counts().reset_index()
player_games.columns = ['player', 'games_played']
threePts = df[['game_id', 'date', 'player', '3_point', '3_point_attempts']]
twoPts = df[['game_id', 'date', 'player', 'field_goals', 'field_goals_attempts']]
freePts = df[['game_id', 'date', 'player', 'free_throw', 'free_throw_attempts']]
rebound = df[['game_id', 'date', 'player', 'offensive_rebound', 'defensive_rebound', 'total_rebound']]
turnover = df[['game_id', 'date', 'player', 'turnovers']]


nyHospitalTypes = newyorkHospitals['hospital_type'].value_counts().reset_index()
st.dataframe(nyHospitalTypes)
st.markdown('The table above indicates the number of different hospitals in New York, as based on the datasets used in this report. As seen within the chart, the majority of New York hospitals are acute care, followed by psychiatric.')

fig = px.pie(nyHospitalTypes, values='hospital_type', names='index')
st.plotly_chart(fig)
st.markdown('The pie chart above visualizes the distribution of the types of hospitals within New York. Counts of the hospitals can be found by hovering over the percentages.')

st.subheader('Map of NY Hospital Locations')
newyorkHospitals_gps = newyorkHospitals['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
newyorkHospitals_gps['lon'] = newyorkHospitals_gps['lon'].str.strip('(')
newyorkHospitals_gps = newyorkHospitals_gps.dropna()
newyorkHospitals_gps['lon'] = pd.to_numeric(newyorkHospitals_gps['lon'])
newyorkHospitals_gps['lat'] = pd.to_numeric(newyorkHospitals_gps['lat'])
st.map(newyorkHospitals_gps)
st.markdown('The interactive map above can be utilized to explore the locations of New York hospitals. Based on the map data, majority of the hos
