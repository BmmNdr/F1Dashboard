#Drivers Standings Page

import streamlit as st
import pandas as pd

import pages.data.data_cache as cache

#Page Configs
st.set_page_config(page_title="Driver Standings", layout="wide")

#Side Bar Settings
st.markdown("<div style='text-align: center;'> <h1> Driver Standings </h1> </div>", unsafe_allow_html=True)
st.sidebar.markdown("# Driver Standings")

#Page Content

#First Row - First, Second and Third Place
SecondPlaceCol, FirstPlaceCol, ThirdPlaceCol = st.columns([1, 1, 1])

try:
    #Gets the driver standings and displays the first three drivers
    dfDriverStandings = pd.DataFrame(cache.driver_standings(), columns=['name', 'team', 'points'])
    dfDriverStandings.index += 1

    with SecondPlaceCol:
        try:
            SecondPlaceCol.image(image=cache.driver_profile_picture(dfDriverStandings.iloc[1]['name']), width=250, use_column_width=True)
        except Exception as e:
            print(e)
        
        SecondPlaceCol.markdown("<h2 style='text-align: center;'> 🥈 " + dfDriverStandings.iloc[1]['name'] + "</h2>", unsafe_allow_html=True)
        SecondPlaceCol.markdown("<h5 style='text-align: center;'>" + dfDriverStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)
        
    with FirstPlaceCol:
        try:
            FirstPlaceCol.image(image=cache.driver_profile_picture(dfDriverStandings.iloc[0]['name']), width=250, use_column_width=True)
        except Exception as e:
            print(e)
        
        FirstPlaceCol.markdown("<h2 style='text-align: center;'> 🥇 " + dfDriverStandings.iloc[0]['name'] + "</h2>", unsafe_allow_html=True)
        FirstPlaceCol.markdown("<h5 style='text-align: center;'>" + dfDriverStandings.iloc[0]['points'] + " pts </h5>", unsafe_allow_html=True)
        
    with ThirdPlaceCol:
        try:
            ThirdPlaceCol.image(image=cache.driver_profile_picture(dfDriverStandings.iloc[2]['name']), width=250, use_column_width=True)
        except Exception as e:
            print(e)
        
        ThirdPlaceCol.markdown("<h2 style='text-align: center;'> 🥉 " + dfDriverStandings.iloc[2]['name'] + "</h2>", unsafe_allow_html=True)
        ThirdPlaceCol.markdown("<h5 style='text-align: center;'>" + dfDriverStandings.iloc[2]['points'] + " pts </h5>", unsafe_allow_html=True)

    #Second Row - Table with all Drivers but the first three
    st.table(dfDriverStandings.iloc[3:])
    
except Exception as e:
    print(e)
    st.text("Error loading Driver Standings")