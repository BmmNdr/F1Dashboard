import streamlit as st
import pandas as pd
import datetime

import pages.data.data_cache as cache


#page configs
st.set_page_config(page_title="Last Race", layout="wide")

#Side bar
st.sidebar.markdown("# Last Race")

# Get Last Race
race_name, year = cache.last_race()

#Get Race Best Laps
fastest_lap, best_laps, team_colors, session = cache.get_fastest_laps(race_name, year)
st.markdown(f"<div style='text-align: center;'> <h1> {session} </h1> </div>", unsafe_allow_html=True)

# Display Race Results
result = cache.get_race_results(race_name, year).reset_index(drop=True)

st.markdown(f"<div style='text-align: center;'> <h3> Race Results </h3> </div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    col1.image(image=cache.driver_profile_picture(result.iloc[1]['Name']), width=100, use_column_width=True)
    col1.markdown("<h2 style='text-align: center;'> 🥈 " + result.iloc[1]['Name'] + "</h2>", unsafe_allow_html=True)
    
with col2:
    col2.image(image=cache.driver_profile_picture(result.iloc[0]['Name']), width=100, use_column_width=True)
    col2.markdown("<h2 style='text-align: center;'> 🥇 " + result.iloc[0]['Name'] + "</h2>", unsafe_allow_html=True)
    
with col3:
    col3.image(image=cache.driver_profile_picture(result.iloc[2]['Name']), width=100, use_column_width=True)
    col3.markdown("<h2 style='text-align: center;'> 🥉 " + result.iloc[2]['Name'] + "</h2>", unsafe_allow_html=True)

result.index += 1
st.table(result)

fastLapCol, charCol = st.columns([1, 2])

#Display fastest Lap
with fastLapCol:
    fastest_lap_time = datetime.datetime(1,1,1,0,0,0) + fastest_lap['LapTime']
    st.markdown(f"<div style='text-align: center;'> <h2> Fastest Lap</h2> </div>", unsafe_allow_html=True)
    
    fastest_driver_name = result[result['Abbreviation'] == fastest_lap['Driver']]['Name'].values[0]
    st.image(image=cache.driver_profile_picture(fastest_driver_name))
    
    st.markdown(f"<h4 style='text-align: center;'> {fastest_lap_time.strftime('%M:%S.%f')[:-3]} by {fastest_lap['Driver']} {fastest_lap['DriverNumber']} </h4>", unsafe_allow_html=True)
    
    

#Display Best Laps
with charCol:
    fig = cache.get_best_laps_fig(best_laps, team_colors)
    st.plotly_chart(fig, use_container_width=True)