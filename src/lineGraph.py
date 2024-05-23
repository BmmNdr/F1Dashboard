from taipy.gui import Gui
import taipy.gui.builder as tgb
from taipy.gui import notify
import plotly.graph_objects as go
import pandas as pd

text = "Testo"
dataframe = pd.DataFrame({"Text":[1, 2],
                          "Score Pos":[1, 2],
                          "Score Neu":[2, 3],
                          "Score Neg":[3, 4],})
bool_variable = True


def on_button_action(state):
    notify(state, 'info', f'The text is: {state.text}')
    state.text = "Button Pressed"

def on_change(state, var_name, var_value):
    if var_name == "text" and var_value == "Reset":
        state.text = ""
        return

with tgb.Page() as page:
    with tgb.layout(columns="1 1"):
        with tgb.part():
            tgb.text("My text: {text}")
            tgb.input("{text}")

        with tgb.expandable("Table"):
            tgb.table("{dataframe}", number_format="%.2f")

    with tgb.layout(columns="1 1 1"):
        with tgb.part():
            tgb.text("## Positive", mode="md")
            tgb.text("{np.mean(dataframe['Score Pos'])}", format="%.2f")
        with tgb.part():
            tgb.text("## Neutral", mode="md")
            tgb.text("{np.mean(dataframe['Score Neu'])}", format="%.2f")
        with tgb.part():
            tgb.text("## Negative", mode="md")
            tgb.text("{np.mean(dataframe['Score Neg'])}", format="%.2f")

    tgb.chart("{dataframe}", x="Text", y__1="Score Pos", y__2="Score Neu", y__3="Score Neg", y__4="Overall",
            color__1="green", color__2="grey", color__3="red", type__4="line")
    

Gui(page).run(debug=True, reload=True)