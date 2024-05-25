import BestLaps as bl
import Standings as st
import NextRace as nr

from taipy.gui import Gui
from taipy.gui import Html
import taipy.gui.builder as tgb
import pandas as pd
import datetime

dfDriverStandingsIndex = pd.DataFrame(st.get_driver_standings())
dfTeamStandingsIndex = pd.DataFrame(st.get_team_standings())

next_race = nr.get_next_race_info()

# Definition of the page
with tgb.Page() as index:

    with tgb.layout(columns="1", id="nextRace"):
        with tgb.part():
            tgb.text(f"Next Race: {next_race['name']} ")
            
            days_remaining, hours_remaining, minutes_remaining = nr.coutdown_to_next(next_race['date'])
            
            with tgb.part():
                tgb.text(f"in {days_remaining} days, {hours_remaining} hours, {minutes_remaining} minutes", style="font-size: 10px; text-align: center;")
            
    with tgb.layout(columns="1 1 2"):
        with tgb.part():
            tgb.text("Driver Standings", style="text-align: center;")
            tgb.table("{dfDriverStandingsIndex}", columns=['position', 'name'], title="Driver Standings")
        
        with tgb.part():
            tgb.text("Team Standings", style="text-align: center;")
            tgb.table("{dfTeamStandingsIndex}", columns=['position', 'team'], title="Team Standings")

with tgb.Page() as DriverStandings:
    tgb.table("{dfDriverStandingsIndex}", title="Driver Standings")
    
with tgb.Page() as TeamStandings:
    tgb.table("{dfTeamStandingsIndex}", title="Team Standings")
    
with tgb.Page() as LastRace: 
    fig = bl.get_fastest_laps_fig()
    
    with tgb.part():
            tgb.chart(figure="{fig}", title="Fastest Laps")

pages = {"/":"<center id='navbar'>\n<|navbar|>\n</center>",
         "Dashboard":index,
         "Driver_Standings": DriverStandings,
         "Team_Standings": TeamStandings,
         "Last_Race": LastRace
         }

Gui(pages=pages, css_file="style.css").run(debug=True, title="F1 Dashboard", dark_mode=False)