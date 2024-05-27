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
    col2.text("🥈 " + dfDriverStandings.iloc[1]['name'])
    
with col2:
    col1.text("🥇 " + dfDriverStandings.iloc[0]['name'])
    
with col3:
    col3.text("🥉 " + dfDriverStandings.iloc[2]['name'])


st.table(dfDriverStandings)