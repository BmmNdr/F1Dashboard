import lastRaceDriverFastLap as lrfl
import Standings as st
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
import pandas as pd

fig = lrfl.get_fastest_laps_fig()

DriverStandings = st.get_driver_standings()
TeamStandings = st.get_team_standings()

dfDriverStandingsIndex = pd.DataFrame(DriverStandings)
dfTeamStandingsIndex = pd.DataFrame(TeamStandings)

# Definition of the page
with tgb.Page() as index:

    with tgb.layout(columns="1 1 1 1"):
        with tgb.part():
            tgb.table("{dfDriverStandingsIndex}", columns=['position', 'name'], title="Driver Standings")
        
        with tgb.part():
            tgb.table("{dfTeamStandingsIndex}", columns=['position', 'team'], title="Team Standings")

    with tgb.layout(columns="2 1 1"):
        with tgb.part():
            tgb.chart(figure="{fig}", title="Fastest Laps")

with tgb.Page() as DriverStandings:
    tgb.table("{dfDriverStandingsIndex}", title="Driver Standings")
    
with tgb.Page() as TeamStandings:
    tgb.table("{dfTeamStandingsIndex}", title="Team Standings")

pages = {"/":"<|toggle|theme|>\n<center>\n<|navbar|>\n</center>",
         "Dashboard":index,
         "Driver_Standings": DriverStandings,
         "Team_Standings": TeamStandings,}

Gui(pages=pages).run(debug=True)