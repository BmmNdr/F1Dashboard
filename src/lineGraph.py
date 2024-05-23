from taipy.gui import Gui
import taipy.gui.builder as tgb
from taipy.gui import notify
import plotly.graph_objects as go
import pandas as pd

import lastRaceDriverFastLap as lr

text = "Testo"
dataframe = lr.test()
bool_variable = True

with tgb.Page() as page:
    tgb.chart("{dataframe}", "bar", x="LapTimeDelta", y="Driver", color="Team", title="Fastest Laps")
    

Gui(page).run(debug=True, reload=True)