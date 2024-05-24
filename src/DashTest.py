import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import lastRaceDriverFastLap as lrfl

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = lrfl.get_fastest_laps_fig()

app.layout = dbc.Container([
    dbc.Row([
        html.H1('F1 Dashboard', className="text-primary text-center fs-3")
    ]),
    
    
    dbc.Row([
        #Last Race Best Laps Section
        dbc.Col([
            html.H4("Last Race Drivers Best Lap", style={'text-align': 'center', 'margin': 'auto', 'padding': '10px', 'color': 'Black'}),
            dcc.Graph(id='bar-graph', figure=fig),
        ], style={'width': 'fit-content', 'display': 'inline-block', 'border': '1px solid black', 'overflow': 'auto'}),
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True)