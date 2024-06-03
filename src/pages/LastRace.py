#Displays the last race information (Results, Best Laps, Tyre Strategy...)

import streamlit as st
import pandas as pd
import datetime

import pages.data.data_cache as cache

#Page Configs
st.set_page_config(page_title="Last Race", layout="wide")


#Side Bar Settings
st.sidebar.markdown("# Last Race")

st.sidebar.markdown("[Result](#race-results)", unsafe_allow_html=True)
st.sidebar.markdown("[Best Laps](#best-laps)", unsafe_allow_html=True)
st.sidebar.markdown("[Tyre Strategy](#tyre-strategy)", unsafe_allow_html=True)


#Page Content

#Creates the Race object
race_name, year = cache.last_race()
race = cache.get_Race(race_name, year)

#Diplay Race (session) Name
st.markdown(f"<div style='text-align: center;'> <h1> {race.session} </h1> </div>", unsafe_allow_html=True)

#Race Results Section
try:
    # Display Race Results
    st.markdown(f"<div style='text-align: center;'> <h3> Race Results </h3> </div>", unsafe_allow_html=True)
    
    #First Row - First, Second and Third Place
    SecondPlaceCol, FirstPlaceCol, ThirdPlaceCol = st.columns([1, 1, 1])

    with SecondPlaceCol:
        try:
            SecondPlaceCol.image(image=cache.driver_profile_picture(race.results.iloc[1]['Name']), width=100, use_column_width=True)
        except Exception as e:
            print(e)
        
        SecondPlaceCol.markdown("<h2 style='text-align: center;'> 🥈 " + race.results.iloc[1]['Name'] + "</h2>", unsafe_allow_html=True)
        
    with FirstPlaceCol:
        try:
            FirstPlaceCol.image(image=cache.driver_profile_picture(race.results.iloc[0]['Name']), width=100, use_column_width=True)
        except Exception as e:
            print(e)
            
        FirstPlaceCol.markdown("<h2 style='text-align: center;'> 🥇 " + race.results.iloc[0]['Name'] + "</h2>", unsafe_allow_html=True)
        
    with ThirdPlaceCol:
        try:
            ThirdPlaceCol.image(image=cache.driver_profile_picture(race.results.iloc[2]['Name']), width=100, use_column_width=True)
        except Exception as e:
            print(e)
        
        ThirdPlaceCol.markdown("<h2 style='text-align: center;'> 🥉 " + race.results.iloc[2]['Name'] + "</h2>", unsafe_allow_html=True)


    #Second Row - Table with all Drivers
    st.table(race.results)
    
except Exception as e:
    st.text("No Data Found")
    print(e)

#Best Laps Section
st.markdown(f"<div style='text-align: center;'> <h3> Best Laps </h3> </div>", unsafe_allow_html=True)

fastLapCol, chartCol = st.columns([1, 1])

try:
    #Display the fastest Lap
    with fastLapCol:
        fastest_lap_time = datetime.datetime(1,1,1,0,0,0) + race.fastest_lap['LapTime']
        fastLapCol.markdown(f"<div style='text-align: center;'> <h2> Fastest Lap</h2> </div>", unsafe_allow_html=True)
        
        try:
            fastLapCol.pyplot(race.heatmap, use_container_width=True)
        except Exception as e:
            print(e)
            fastest_driver_name = race.results[race.results['Abbreviation'] == race.fastest_lap['Driver']]['Name'].values[0]
            fastLapCol.image(image=cache.driver_profile_picture(fastest_driver_name))
        
        fastLapCol.markdown(f"<h4 style='text-align: center;'> {fastest_lap_time.strftime('%M:%S.%f')[:-3]} by {race.fastest_lap['Driver']} {race.fastest_lap['DriverNumber']} </h4>", unsafe_allow_html=True)
        
        
    #Display Best Laps DeltaTime
    with chartCol:
        chartCol.plotly_chart(race.fig, use_container_width=True)
        
except Exception as e:
    print(e)
    st.text("No Data Found")
    
    
#Tyre Strategy Section
st.markdown(f"<div style='text-align: center;'> <h3> Tyre Strategy </h3> </div>", unsafe_allow_html=True)

try:
    # Display Tyre Strategy
    st.pyplot(race.tyre_strategy, use_container_width=True)
except Exception as e:
    print(e)
    st.text("No Data Found")