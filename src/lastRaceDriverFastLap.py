import matplotlib.pyplot as plt
import pandas as pd
import fastf1 as ff1
import fastf1.plotting as ff1plt
from fastf1.core import Laps
import datetime
import requests
import plotly.express as px


def get_last_f1_race(year):
    url = f"https://api.openf1.org/v1/meetings?year={year}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            if data:
                last_race = data[-1]  # Assuming the last item in the list is the latest race
                race_name = last_race.get("meeting_name")
                
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

def get_fastest_laps():
    race_name, year = get_last_f1_race(datetime.datetime.now().year)

    if(race_name != None):
        session = ff1.get_session(year, race_name, 'R')
        session.load()

        drivers = pd.unique(session.laps['Driver'])

        list_fastest_laps = list()
        for drv in drivers:
            drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)


        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

        pole_lap = fastest_laps.pick_fastest()
        pole_lap_time = datetime.datetime(1,1,1,0,0,0) + pole_lap['LapTime']


        fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']


        team_colors = list()

        for index, lap in fastest_laps.iterlaps():

            try:
                color = ff1plt.team_color(lap['Team'])
            except:
                color = 'black'    

            team_colors.append(color)
            
        return pole_lap_time, pole_lap, fastest_laps, team_colors, session

def plot_with_matplotlib(pole_lap_time, pole_lap, fastest_laps, team_colors, session):
    fig, ax = plt.subplots()

    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # Show fastest at the top
    ax.invert_yaxis()

    # Draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    # Title for the plot
    lap_time_string = pole_lap_time.strftime('%M:%S.%f')[:-3]
    plt.suptitle(f"{session.event['EventName']} {session.event.year} Race\n"
                 f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

    plt.show()
    
def get_fastest_laps_fig():
    pole_lap_time, pole_lap, fastest_laps, team_colors, session = get_fastest_laps()

    lap_time_string = pole_lap_time.strftime('%M:%S.%f')[:-3]

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
        title={
            'text': f"{session.session_info['Meeting']['Name']}\n\nFastest Lap: {lap_time_string} ({pole_lap['Driver']})",
            'x': 0.5,  # Center the title horizontally
            'y': 0.95  # Position the title near the top of the plot
        },
        showlegend=False  # Remove the legend
    )

    return fig
