import streamlit as st
import datetime

import pages.data.RaceUtility as RaceUtility
import pages.data.StandingsUtility as StandingsUtility

from pages.data.CRace import Race

@st.cache_data(ttl="2d", show_spinner="Fetching Driver Standings...")
def driver_standings():
    return StandingsUtility.get_driver_standings()

@st.cache_data(ttl="2d", show_spinner="Fetching Team Standings...")
def team_standings():
    return StandingsUtility.get_team_standings()

@st.cache_data(ttl="1d", show_spinner="Getting Next Race...")
def next_race():
    return RaceUtility.get_next_race_info()

@st.cache_data(persist=True, show_spinner="Fetching Driver Profile Picture...")
def driver_profile_picture(driver_name, year = None):
    return StandingsUtility.get_driver_profile_picture(driver_name, year)

@st.cache_data(persist=True, show_spinner="Fetching Team Profile Picture...")
def team_profile_picture(team):
    return StandingsUtility.get_team_profile_picture(team)

@st.cache_data(ttl="2d", show_spinner="Getting Last Race Info...")
def last_race():
    return RaceUtility.get_last_f1_race(datetime.datetime.now().year)

#Returns an object of type Race
@st.cache_data(persist=True, show_spinner="Fetching Race Data...")
def get_Race(race_name, race_year):
    try:
        return Race(race_name, race_year)
    except Exception as e:
        print(e)
        return None