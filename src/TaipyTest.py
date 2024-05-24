import lastRaceDriverFastLap as lrfl
import Standings as st
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
import pandas as pd

fig = lrfl.get_fastest_laps_fig()

dfDriverStandings = pd.DataFrame(st.get_driver_standings())
colDriverStandings = ['position', 'name', 'nationality', 'team', 'points']
dfTeamStandings = pd.DataFrame(st.get_team_standings())
colTeamStandings = ['position', 'team', 'points']

# Definition of the page
with tgb.Page() as page:

    with tgb.layout(columns="1 1"):
        with tgb.part():
            tgb.text("Driver Standings", size="h2")
            tgb.table("{dfDriverStandings}", title="Driver Standings")
        
        with tgb.part():
            tgb.text("Team Standings", size="h2")
            tgb.table("{dfTeamStandings}", title="Team Standings")
    
    tgb.chart(figure="{fig}", title="Fastest Laps")

Gui(page).run(debug=True)