import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

import Standings
import NextRace

#page configs
st.set_page_config(page_title="My F1 Dashboard", page_icon="🏎️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .centered-title {
        text-align: center;
        font-size: 2em;  /* Adjust the font size as needed */
        font-weight: bold;
        margin-bottom: 20px;  /* Adjust the margin as needed */
    }
    .dataframe-container {
        height: 600px;
        width: 100%;
        overflow: auto;
    }
    .dataframe-container table {
        width: 100%;
        font-size: 16px;  /* Adjust font size */
    }
    
    #countdown-clock-wrapper {
    -webkit-font-smoothing: antialiased;
    font-family: "Titillium Web";
    font-size: 17px;
    line-height: 23px;
    letter-spacing: -.1px;
    box-sizing: border-box;
    display: table-cell;
    background-color: #006341;
    border-radius: 10px;
    vertical-align: middle;
    margin: 0 auto;
}

#countdown-clock {
    -webkit-font-smoothing: antialiased;
    font-family: "Titillium Web";
    font-size: 17px;
    line-height: 23px;
    letter-spacing: -.1px;
    box-sizing: border-box;
    display: table-cell;
    background-color: #006341;
    vertical-align: middle;
    padding: 20px;
    border-radius: 50px;
}

#title-bar {
        -webkit-font-smoothing: antialiased;
    letter-spacing: -.1px;
    box-sizing: border-box;
    text-transform: uppercase;
    text-align: center;
    color: #fff;
    border-bottom: 1px solid rgba(208,208,210,.4);
    font-family: F1Bold;
    font-size: 13px;
    line-height: 14px;
    width: 100%;
    padding-bottom: 6px;
    margin-bottom: 14px;
}

#clock {
    -webkit-font-smoothing: antialiased;
    font-family: "Titillium Web";
    font-size: 17px;
    line-height: 23px;
    letter-spacing: -.1px;
    box-sizing: border-box;
    display: table;
    margin: 0 auto;
    white-space: nowrap;
    font-feature-settings: "tnum";
}

#time {
        -webkit-font-smoothing: antialiased;
    font-family: "Titillium Web";
    font-size: 17px;
    line-height: 23px;
    letter-spacing: -.1px;
    white-space: nowrap;
    font-feature-settings: "tnum";
    box-sizing: border-box;
    display: table-cell;
    color: #fff;
    padding: 0 10px;
    text-align: center;
    padding-left: 0;
    border-left: 0;
}

#text {
        -webkit-font-smoothing: antialiased;
    white-space: nowrap;
    font-feature-settings: "tnum";
    text-align: center;
    box-sizing: border-box;
    margin-top: 0;
    color: #fff;
    font-family: F1Bold;
    font-size: 28px;
    letter-spacing: -.76px;
    margin-bottom: 0;
    line-height: 1;
}

#f1-uppercase {
        -webkit-font-smoothing: antialiased;
    letter-spacing: -.1px;
    white-space: nowrap;
    font-feature-settings: "tnum";
    text-align: center;
    box-sizing: border-box;
    text-transform: uppercase;
    display: block;
    font-family: "Titillium Web";
    font-size: 13px;
    line-height: 17px;
    color: rgba(255,255,255,.7);
    font-weight: 600;
}

.centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
     .dataframe .row_heading.level0, .dataframe .blank {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

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

#page

# Title and description
st.markdown('<h1 class="centered-title">My F1 Dashboard</h1>', unsafe_allow_html=True)

colDriverStandings, colTeamStandings, colNextRace = st.columns([1, 1, 2], gap="large")

colDriverStandings.header("Driver Standings")
colTeamStandings.header("Team Standings")

with colDriverStandings:
    dfDriverStandingsIndex = pd.DataFrame(driver_standings(), columns=['name', 'points'])
    dfDriverStandingsIndex.index += 1
    st.table(dfDriverStandingsIndex)
    
with colTeamStandings:
    dfTeamStandingsIndex = pd.DataFrame(team_standings(), columns=['team'])
    dfTeamStandingsIndex.index += 1
    st.table(dfTeamStandingsIndex)
    
with colNextRace:
    race = next_race()
    
    colNextRace.header("Next Race: " + race['name'])
    
    # Use st_autorefresh to refresh the countdown every 10 seconds
    countdown_autorefresh = st_autorefresh(interval=5 * 1000, key="countdown_refresh")

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