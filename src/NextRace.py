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
        'date': schedule.Session5DateUtc[index].strftime('%Y-%m-%d'),
        'time': schedule.Session5DateUtc[index].strftime('%H:%M:%S') if schedule.Session5DateUtc[index] else 'TBD'
    }

    return race_info

# Example usage
if __name__ == "__main__":
    next_race = get_next_race_info()
    print(next_race)
