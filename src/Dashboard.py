#streamlit run src/Dashboard.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

import pages.data.data_cache as cache
import pages.data.NextRace as NextRace

#page configs
st.set_page_config(page_title="My F1 Dashboard", page_icon="🏎️", layout="wide")

#Side bar
st.markdown("<div style='text-align: center;'> <h1> F1 Dashboard 🏎️ </h1> </div>", unsafe_allow_html=True)
st.sidebar.markdown("# Dashboard")

# Custom CSS
with open("src/pages/css/indexStyle.html", "r") as file:
    css = file.read()

st.markdown(css, unsafe_allow_html=True)

#page content
colDriverStandings, colTeamStandings, colNextRace = st.columns([1, 1, 2], gap="large")

colDriverStandings.header("Driver Standings")
colTeamStandings.header("Team Standings")

with colDriverStandings:
    dfDriverStandingsIndex = pd.DataFrame(cache.driver_standings(), columns=['name', 'points'])
    dfDriverStandingsIndex.index += 1
    st.table(dfDriverStandingsIndex)
    
with colTeamStandings:
    dfTeamStandingsIndex = pd.DataFrame(cache.team_standings(), columns=['team'])
    dfTeamStandingsIndex.index += 1
    st.table(dfTeamStandingsIndex)
    
with colNextRace:
    race = cache.next_race()
    
    colNextRace.header("Next Race: " + race['name'])
    
    # Use st_autorefresh to refresh the countdown every 10 seconds
    countdown_autorefresh = st_autorefresh(interval=1000, key="countdown_refresh")

    countdown = NextRace.countdown_to_next(race['date'], race['time'])
    countdown_text = f"{countdown['days']} days, {countdown['hours']} hours, {countdown['minutes']} minutes, {countdown['seconds']} seconds"
    
    colNextRace.image("src/images/layouts/" + race['location'] + ".png")
    
    # Display the countdown in the same way as the Formula 1 official site
    colNextRace.markdown(f"""
                         <div class="centered-content">
        <div id="countdown-clock-wrapper">
                        <div id="countdown-clock">
                            <div id="title-bar">{race['location']} Race</div>
                            <div id="clock">
                                <div id="time">
                                    <p id="text">{countdown['days']}</p>
                                    <span id="f1-uppercase">days</span>
                                </div>
                                <div id="time">
                                    <p id="text">{countdown['hours']}</p>
                                    <span id="f1-uppercase">hrs</span>
                                </div>
                                <div id="time">
                                    <p id="text">{countdown['minutes']}</p>
                                    <span id="f1-uppercase">mins</span>
                                </div>
                                <div id="time">
                                    <p id="text">{countdown['seconds']}</p>
                                    <span id="f1-uppercase">secs</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
    """, unsafe_allow_html=True)
    


#Display Last Race Result
st.markdown("<div style='text-align: center;'> <h1> Last Race Results </h1> </div>", unsafe_allow_html=True)

resultCol, winnerCol = st.columns([2, 1])

with resultCol:
    # Display Race Results
    race_name, year = cache.last_race()
    result = cache.get_race_results(race_name, year).reset_index(drop=True)
    result.index += 1

    st.table(pd.DataFrame(result, columns=['Name', 'Team']))
    
with winnerCol:
    #Display Winner Image
    winner = result.iloc[0]['Name']
    
    st.markdown(f"<div style='text-align: center;'> <h1> The Winner is {winner.split(" ")[1]} </h1> </div>", unsafe_allow_html=True)
    
    winner_image = cache.driver_profile_picture(winner)
    st.image(winner_image, use_column_width=True)