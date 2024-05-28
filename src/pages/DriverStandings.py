import streamlit as st
import pandas as pd

import pages.data.data_cache as cache


#page configs
st.set_page_config(page_title="Driver Standings", layout="wide")

#Side bar
st.markdown("<div style='text-align: center;'> <h1> Driver Standings </h1> </div>", unsafe_allow_html=True)
st.sidebar.markdown("# Driver Standings")

col1, col2, col3 = st.columns([1, 1, 1])

dfDriverStandings = pd.DataFrame(cache.driver_standings(), columns=['name', 'team', 'points'])
dfDriverStandings.index += 1

with col1:
    col1.image(image=cache.driver_profile_picture(dfDriverStandings.iloc[1]['name']), width=250, use_column_width=True)
    col1.markdown("<h2 style='text-align: center;'> 🥈 " + dfDriverStandings.iloc[1]['name'] + "</h2>", unsafe_allow_html=True)
    col1.markdown("<h5 style='text-align: center;'>" + dfDriverStandings.iloc[1]['points'] + " pts </h5>", unsafe_allow_html=True)
    
with col2:
    col2.image(image=cache.driver_profile_picture(dfDriverStandings.iloc[0]['name']), width=250, use_column_width=True)
    col2.markdown("<h2 style='text-align: center;'> 🥇 " + dfDriverStandings.iloc[0]['name'] + "</h2>", unsafe_allow_html=True)
    col2.markdown("<h5 style='text-align: center;'>" + dfDriverStandings.iloc[0]['points'] + " pts </h5>", unsafe_allow_html=True)
    
with col3:
    col3.image(image=cache.driver_profile_picture(dfDriverStandings.iloc[2]['name']), width=250, use_column_width=True)
    col3.markdown("<h2 style='text-align: center;'> 🥉 " + dfDriverStandings.iloc[2]['name'] + "</h2>", unsafe_allow_html=True)
    col3.markdown("<h5 style='text-align: center;'>" + dfDriverStandings.iloc[2]['points'] + " pts </h5>", unsafe_allow_html=True)

st.table(dfDriverStandings.iloc[3:])