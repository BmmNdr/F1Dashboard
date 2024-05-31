import matplotlib.pyplot as plt
import pandas as pd
import fastf1 as ff1
import fastf1.plotting as ff1plt
from fastf1.core import Laps
import requests
import plotly.express as px
import datetime
import matplotlib as mpl
import numpy as np
from matplotlib.collections import LineCollection
import re

def rreplace(s, old, new):
    return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

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

    lap = best_laps.pick_fastest()
    
    driver = lap['Driver']
    
    fastest_lap = session.laps.pick_driver(driver).pick_fastest()

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

def get_fastest_lap_heatmap(fastest_lap):
    colormap = mpl.cm.plasma
    
    # Get telemetry data
    x = fastest_lap.telemetry['X']              # values for x-axis
    y = fastest_lap.telemetry['Y']              # values for y-axis
    color = fastest_lap.telemetry['Speed']      # value to base color gradient on
    
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    # After this, we plot the data itself.
    # Create background track line
    ax.plot(fastest_lap.telemetry['X'], fastest_lap.telemetry['Y'],
            color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(color.min(), color.max())
    lc = LineCollection(segments, cmap=colormap, norm=norm,
                        linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)


    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap,
                                    orientation="horizontal")

    # Show the plot
    return fig

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

def get_race_result(year, race_name):
    # Get the race session
    session = ff1.get_session(year, race_name, 'R')

    # Load session results
    session.load()
    
    # Modify and format the Time
    modified_time = []
    for time, status in zip(session.results['Time'], session.results['Status']):
        if status == 'Finished':
                        
            dt = (datetime.datetime(1,1,1,0,0,0) + time)
        
            if(modified_time != []):
                # Extract components
                hour = dt.hour
                minute = dt.minute
                second = dt.second
                
                # Calculate total seconds
                total_seconds = hour * 3600 + minute * 60 + second
                milliseconds = dt.microsecond // 1000  # Convert microseconds to milliseconds

                # Format the string
                formatted_time = f"{total_seconds}.{milliseconds:03}"
                
                modified_time.append("+" + formatted_time)
            else:
             formatted_time = dt.strftime("%H:%M:%S:%f").lstrip("0").lstrip(":").rstrip("0").rstrip(":")
             modified_time.append(rreplace(formatted_time, ":", "."))
             
        else:
            modified_time.append(status)

    df = pd.DataFrame({
        'Name': session.results["BroadcastName"],
        'Number': session.results["DriverNumber"],
        'Abbreviation': session.results["Abbreviation"],
        'Team': session.results['TeamName'],
        'Grid Position': [str(position).split('.')[0] for position in session.results['GridPosition']],
        'Time': modified_time
    })

    return df

def tyre_strategy(year, race_name):
    # Get the race session
    session = ff1.get_session(year, race_name, 'R')

    # Load session results
    session.load()

    # Extract pit stop data
    laps = session.laps
    
    # Define tire compound colors
    compound_colors = {
        'SOFT': 'red',
        'MEDIUM': 'yellow',
        'HARD': 'white',
        'INTERMEDIATE': 'green',
        'WET': 'blue',
    }

    # Extract unique drivers
    drivers = laps['Driver'].unique()

    driver_mapping = {driver: idx for idx, driver in enumerate(drivers)}

    fig, ax = plt.subplots(figsize=(15, 10))

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Plot tire compounds for each lap and each driver
    for driver in drivers:
        driver_laps = laps[laps['Driver'] == driver]
        driver_idx = driver_mapping[driver]

        # Initialize variables for tracking tire changes
        prev_compound = None
        prev_lap = None

        for lap in driver_laps.itertuples():
            compound = lap.Compound

            # Plot a dot only if there's a tire change
            if compound != prev_compound:
                if prev_lap is not None:
                    ax.plot([prev_lap, lap.LapNumber], [driver_idx, driver_idx], color=compound_colors.get(prev_compound, 'black'), linewidth=2)
                ax.plot(lap.LapNumber, driver_idx, marker='o', color=compound_colors.get(compound, 'black'))
                prev_lap = lap.LapNumber

            prev_compound = compound

        # If the race ended without a tire change, draw a line segment to the end of the race
        if prev_lap is not None and prev_lap < len(driver_laps):
            ax.plot([prev_lap, len(driver_laps)], [driver_idx, driver_idx], color=compound_colors.get(prev_compound, 'black'), linewidth=2)
            ax.plot(len(driver_laps), driver_idx, marker='o', color=compound_colors.get(prev_compound, 'black'))

    # Set labels and title
    ax.set_xlabel('Lap Number', color='white')
    ax.set_ylabel('Driver', color='white')
    ax.set_title('Tire Compound Usage by Driver and Lap', color='white')
    ax.grid(True, color='gray')
    ax.set_yticks(list(driver_mapping.values()))
    ax.set_yticklabels(list(driver_mapping.keys()), color='white')
    ax.set_xticklabels(ax.get_xticks(), color='white')
    ax.invert_yaxis()  # Invert y-axis to have the first driver on top

    # Create a legend for tire compounds
    handles = [plt.Line2D([0], [0], marker='o', color=color, linestyle='', label=compound)
               for compound, color in compound_colors.items()]
    legend = ax.legend(handles=handles, title='Tire Compounds', facecolor='black', edgecolor='white')
    plt.setp(legend.get_texts(), color='white')
    plt.setp(legend.get_title(), color='white')
    
    return fig