import streamlit as st
import pandas as pd
import datetime

import pages.data.data_cache as cache


#page configs
st.set_page_config(page_title="Last Race", layout="wide")

#Side bar
st.sidebar.markdown("# Last Race")

#Get Race Best Laps
fastest_lap, best_laps, team_colors, session = cache.get_fastest_laps(*cache.last_race())
st.markdown(f"<div style='text-align: center;'> <h1> {session} </h1> </div>", unsafe_allow_html=True)

#Display fastest Lap
fastest_lap_time = datetime.datetime(1,1,1,0,0,0) + fastest_lap['LapTime']
st.markdown(f"<div style='text-align: center;'> <h2> Fastest Lap: {fastest_lap_time.strftime('%M:%S.%f')[:-3]} by {fastest_lap['Driver']} {fastest_lap['DriverNumber']}</h2> </div>", unsafe_allow_html=True)

#Display Best Laps
fig = cache.get_best_laps_fig(best_laps, team_colors)
st.plotly_chart(fig, use_container_width=True)