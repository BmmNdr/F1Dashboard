import streamlit as st
import pages.data.NextRace as NextRace
import pages.data.Standings as Standings


#chached data
@st.cache_data
def driver_standings():
    return Standings.get_driver_standings()

@st.cache_data
def team_standings():
    return Standings.get_team_standings()

@st.cache_data
def next_race():
    return NextRace.get_next_race_info()