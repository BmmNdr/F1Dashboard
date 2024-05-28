import streamlit as st
import datetime

import pages.data.NextRace as NextRace
import pages.data.Standings as Standings
import pages.data.ImagePicture as ImagePicture
import pages.data.BestLaps as BestLaps

#chached data
@st.cache_data(ttl="2d")
def driver_standings():
    return Standings.get_driver_standings()

@st.cache_data(ttl="2d")
def team_standings():
    return Standings.get_team_standings()

@st.cache_data(ttl="1d")
def next_race():
    return NextRace.get_next_race_info()

@st.cache_data
def driver_profile_picture(driver_name):
    return ImagePicture.get_driver_profile_picture(driver_name)

@st.cache_data
def team_profile_picture(team):
    return ImagePicture.get_team_profile_picture(team)

@st.cache_data(ttl="2d")
def last_race():
    return BestLaps.get_last_f1_race(datetime.datetime.now().year)

@st.cache_data
def get_fastest_laps(race_name, year):
    return BestLaps.get_fastest_laps(year, race_name)