#Team Standings Page

import streamlit as st
import pandas as pd

import pages.data.data_cache as cache

#Page Configs
st.set_page_config(page_title="Constructors Standings", layout="wide")

#Side Bar Settings
st.markdown("<div style='text-align: center;'> <h1> Constructors Standings </h1> </div>", unsafe_allow_html=True)
st.sidebar.markdown("# Constructors Standings")

#Page Content

#First Row - First, Second and Third Place
SecondPlaceCol, FirstPlaceCol, ThirdPlaceCol = st.columns([1, 1, 1])

try:
    #Gets the team standings and displays the first three teams
    dfTeamStandings = pd.DataFrame(cache.team_standings(), columns=['team', 'points'])
    dfTeamStandings.index += 1

    with SecondPlaceCol:
        try:
            SecondPlaceCol.image(image=cache.team_profile_picture(dfTeamStandings.iloc[1]['team']), width=300, use_column_width=True)
        except Exception as e:
            print(e)
            
        SecondPlaceCol.markdown("<h2 style='text-align: center;'> 🥈 " + dfTeamStandings.iloc[1]['team'] + "</h2>", unsafe_allow_html=True)
        SecondPlaceCol.markdown("<h5 style='text-align: center;'>" + dfTeamStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)
        
    with FirstPlaceCol:
        try:
            FirstPlaceCol.image(image=cache.team_profile_picture(dfTeamStandings.iloc[0]['team']), width=300, use_column_width=True)
        except Exception as e:
            print(e)
            
        FirstPlaceCol.markdown("<h2 style='text-align: center;'> 🥇 " + dfTeamStandings.iloc[0]['team'] + "</h2>", unsafe_allow_html=True)
        FirstPlaceCol.markdown("<h5 style='text-align: center;'>" + dfTeamStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)
        
    with ThirdPlaceCol:
        try:
            ThirdPlaceCol.image(image=cache.team_profile_picture(dfTeamStandings.iloc[2]['team']), width=300, use_column_width=True)
        except Exception as e:
            print(e)
            
        ThirdPlaceCol.markdown("<h2 style='text-align: center;'> 🥉 " + dfTeamStandings.iloc[2]['team'] + "</h2>", unsafe_allow_html=True)
        ThirdPlaceCol.markdown("<h5 style='text-align: center;'>" + dfTeamStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)


    #Second Row - Table with all Teams but the first three
    st.table(dfTeamStandings.iloc[3:])
except Exception as e:
    st.text("Error loading Team Standings")
    print(e)