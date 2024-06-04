#Use this to run the dashboard locally
#streamlit run src/Dashboard.py

#Index Page
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

import pages.data.Cache as Cache
import pages.data.RaceUtility as RaceUtility

#Page Configuration
st.set_page_config(page_title="My F1 Dashboard", page_icon="🏎️", layout="wide")

#Side Bar Settings
st.markdown("<div style='text-align: center;'> <h1> F1 Dashboard 🏎️ </h1> </div>", unsafe_allow_html=True)
st.sidebar.markdown("# Dashboard")

# Custom CSS
with open("src/pages/css/indexStyle.html", "r") as file:
    css = file.read()
st.markdown(css, unsafe_allow_html=True)

#Page Content

#First Row - Driver Standings, Team Standings and Next Race
colDriverStandings, colTeamStandings, colNextRace = st.columns([1, 1, 2], gap="large")

with colDriverStandings:
    colDriverStandings.header("Driver Standings")
    
    try:
        #Gets the Driver Standings and displays it in a table
        dfDriverStandingsIndex = pd.DataFrame(Cache.driver_standings(), columns=['name', 'points'])
        dfDriverStandingsIndex.index += 1
        colDriverStandings.table(dfDriverStandingsIndex)
    except Exception as e:
        st.text("Error loading Driver Standings")
        print(e)
    
with colTeamStandings:
    colTeamStandings.header("Team Standings")
    
    try:
        #Gets the Team Standings and displays it in a table
        dfTeamStandingsIndex = pd.DataFrame(Cache.team_standings(), columns=['team'])
        dfTeamStandingsIndex.index += 1
        colTeamStandings.table(dfTeamStandingsIndex)
    except Exception as e:
        st.text("Error loading Team Standings")
        print(e)
    
with colNextRace:
    
    try:
        #Gets the Next Race Event
        race = Cache.next_race()
        
        colNextRace.header("Next Race: " + race['name'])

        #Displays the countdown to the next race
        countdown = RaceUtility.countdown_to_next(race['date'], race['time'])
        countdown_text = f"{countdown['days']} days, {countdown['hours']} hours, {countdown['minutes']} minutes, {countdown['seconds']} seconds"
        
        #Shows the track layout image
        try:
            colNextRace.image("src/images/layouts/" + race['location'] + ".png")
        except Exception as e:
            print(e)
        
        #Display the countdown in the same way as in the Formula 1 official site
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
    except Exception as e:
        st.text("Error loading Next Race")
        print(e)
    

#Second Row - Last Race Results
st.markdown("<div style='text-align: center;'> <h1> Last Race Results </h1> </div>", unsafe_allow_html=True)

resultCol, winnerCol = st.columns([2, 1])

try:
    with resultCol:
        race_name, year = Cache.last_race()
        
        #Creates a Race Object
        last_race = Cache.get_Race(race_name, year)

        resultCol.table(pd.DataFrame(last_race.results, columns=['Name', 'Team']))
        
    with winnerCol:
        #Display Winner Image
        winner = last_race.results.iloc[0]['Name']
        
        winnerCol.markdown(f"<div style='text-align: center;'> <h1> The Winner is {winner.split(' ')[1]} </h1> </div>", unsafe_allow_html=True)
        
        try:
            winner_image = Cache.driver_profile_picture(winner)
            winnerCol.image(winner_image, use_column_width=True)
        except Exception as e:
            print(e)
            
except Exception as e:
    st.text("Error loading Last Race Results")
    print(e)
    
#Use st_autorefresh to refresh the countdown every 10 seconds
countdown_autorefresh = st_autorefresh(interval=1000, key="countdown_refresh")