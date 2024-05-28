import streamlit as st
import pages.data.NextRace as NextRace
import pages.data.Standings as Standings
import pages.data.ImagePicture as ImagePicture


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

@st.cache_data
def driver_profile_picture(driver_name):
    return ImagePicture.get_driver_profile_picture(driver_name)

@st.cache_data
def team_profile_picture(team):
    return ImagePicture.get_team_profile_picture(team)