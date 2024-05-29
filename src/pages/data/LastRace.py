import matplotlib.pyplot as plt
import pandas as pd
import fastf1 as ff1
import fastf1.plotting as ff1plt
from fastf1.core import Laps
import datetime
import requests
import plotly.express as px


def get_last_f1_race(year):
    url = f"https://api.openf1.org/v1/sessions?session_name=Race&year={year}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            if data:
                last_race = data[-1]  # Assuming the last item in the list is the latest race
                meeting_key = last_race.get("meeting_key")
                
                url = f"https://api.openf1.org/v1/meetings?meeting_key={meeting_key}"
                data = requests.get(url).json()
                
                race_name = data[0]['meeting_name']
                
                if race_name:
                    return race_name, year
                else:
                    return get_last_f1_race(year - 1)
            else:
                return get_last_f1_race(year - 1)
        else:
            return None
    
    except requests.exceptions.RequestException as e:
        return None

def get_fastest_laps(year, race_name):

    session = ff1.get_session(year, race_name, 'R')
    session.load()

    drivers = pd.unique(session.laps['Driver'])

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)


    best_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    fastest_lap = best_laps.pick_fastest()
    pole_lap_time = datetime.datetime(1,1,1,0,0,0) + fastest_lap['LapTime']


    best_laps['LapTimeDelta'] = best_laps['LapTime'] - fastest_lap['LapTime']

    best_laps = best_laps.dropna(subset=['LapTime'])

    team_colors = list()

    for index, lap in best_laps.iterlaps():

        try:
            color = ff1plt.team_color(lap['Team'])
        except:
            color = 'black'    

        team_colors.append(color)
            
    return fastest_lap, best_laps, team_colors, session
 
 
 

def get_fastest_laps_fig(fastest_laps, team_colors):

    drivers = fastest_laps['Driver'].values
    lap_times = fastest_laps['LapTimeDelta'].values

    df = pd.DataFrame({
        'DeltaTime' : lap_times,
        'Driver' : drivers,
        'Team' : team_colors
    })

    df['DeltaTime'] = pd.to_numeric(df['DeltaTime'])  # Convert 'DeltaTime' column to numeric type

    df = df.sort_values(by='DeltaTime')  # Sort the DataFrame by 'DeltaTime' column

    fig = px.bar(df, y='Driver', x='DeltaTime', color='Team',barmode='group', orientation='h')

    fig.update_layout(
        height=800,  # Set the height of the plot
        width=1000,  # Set the width of the plot
        bargap=0.1,  # Set the gap between bars
        barmode='stack',  # Stack the bars on top of each other
        yaxis={'categoryorder':'array', 'categoryarray': df['Driver']},  # Sort the y-axis categories according to the 'Driver' column
        xaxis={'range': [df['DeltaTime'].min() - 0.5, df['DeltaTime'].max() + 0.5]},  # Set the x-axis range
        yaxis_title='Driver',  # Set the y-axis title
        xaxis_title='DeltaTime',  # Set the x-axis title
        title="Best Laps Delta Time",  # Set the title of the plot
        showlegend=False  # Remove the legend
    )

    return fig