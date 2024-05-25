import fastf1
import datetime
import numpy as np

def get_next_race_info(year = None):
    # Get the current season's schedule
    
    if(year is None):
        year = datetime.datetime.now().year
        
    schedule = fastf1.get_event_schedule(year)

    # Find the next race
    index = 1
    for event in schedule.Session5Date[1:]:
        if event.date() > datetime.datetime.now().date():
            break
        
        index += 1

    if index >  len(schedule.Session5Date) - 1 is None:
        raise Exception("Could not find the next race in the schedule.")

    race_info = {
        'name': schedule.OfficialEventName[index],
        'location': schedule.Location[index],
        'date': schedule.Session5Date[index].strftime('%Y-%m-%d'),
        'time': schedule.Session5Date[index].strftime('%H:%M:%S') if schedule.Session5Date[index] else 'TBD'
    }

    return race_info

def coutdown_to_next(race_date):
    race_date = datetime.datetime.strptime(race_date, "%Y-%m-%d")
    current_date = datetime.datetime.now()
    time_remaining = race_date - current_date  
    
    days_remaining = time_remaining.days
    hours_remaining = time_remaining.seconds // 3600
    minutes_remaining = (time_remaining.seconds % 3600) // 60
    
    return days_remaining, hours_remaining, minutes_remaining