import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

import lastRaceDriverFastLap as lrfl

# Initialize the app
app = dash.Dash(__name__)

fig = lrfl.get_fastest_laps_fig()

app.layout = html.Div(children=[
    html.Div([
        html.H1("Last Race Drivers Best Lap", style={'text-align': 'center'}),
        dcc.Graph(id='bar-graph', figure=fig),
    ], style={'width': '50%', 'display': 'inline-block'}),
])

# Define callback to update graph based on dropdown selection
#@app.callback(
#    dash.dependencies.Output('bar-graph', 'figure'),
#    [dash.dependencies.Input('city-dropdown', 'value')]
#)
#
#def update_graph(selected_city):
#    filtered_df = df[df['City'] == selected_city]
#    fig = px.bar(filtered_df, x='Fruit', y='Amount', color='City', barmode='group')
#    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
