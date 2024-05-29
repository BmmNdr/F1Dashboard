import streamlit as st
import pandas as pd

import pages.data.data_cache as cache

#page configs
st.set_page_config(page_title="Constructors Standings", layout="wide")

#Side bar
st.markdown("<div style='text-align: center;'> <h1> Constructors Standings </h1> </div>", unsafe_allow_html=True)
st.sidebar.markdown("# Constructors Standings")



col1, col2, col3 = st.columns([1, 1, 1])

dfTeamStandings = pd.DataFrame(cache.team_standings(), columns=['team', 'points'])
dfTeamStandings.index += 1

with col1:
    col1.image(image=cache.team_profile_picture(dfTeamStandings.iloc[1]['team']), width=300, use_column_width=True)
    col1.markdown("<h2 style='text-align: center;'> 🥈 " + dfTeamStandings.iloc[1]['team'] + "</h2>", unsafe_allow_html=True)
    col1.markdown("<h5 style='text-align: center;'>" + dfTeamStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)
    
with col2:
    col2.image(image=cache.team_profile_picture(dfTeamStandings.iloc[0]['team']), width=300, use_column_width=True)
    col2.markdown("<h2 style='text-align: center;'> 🥇 " + dfTeamStandings.iloc[0]['team'] + "</h2>", unsafe_allow_html=True)
    col2.markdown("<h5 style='text-align: center;'>" + dfTeamStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)
    
with col3:
    col3.image(image=cache.team_profile_picture(dfTeamStandings.iloc[2]['team']), width=300, use_column_width=True)
    col3.markdown("<h2 style='text-align: center;'> 🥉 " + dfTeamStandings.iloc[2]['team'] + "</h2>", unsafe_allow_html=True)
    col3.markdown("<h5 style='text-align: center;'>" + dfTeamStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)

st.table(dfTeamStandings.iloc[3:])