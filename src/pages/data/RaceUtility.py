import requests
import fastf1
import datetime

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
        'name': schedule.OfficialEventName[index].replace(str(year), ''),
        'location': schedule.Location[index],
        'date': schedule.Session5Date[index].strftime('%Y-%m-%d'),
        'time': schedule.Session5Date[index].strftime('%H:%M:%S') if schedule.Session5Date[index] else 'TBD'
    }

    return race_info

def countdown_to_next(race_date, race_time):
    race_datetime = datetime.datetime.strptime(race_date + ' ' + race_time, "%Y-%m-%d %H:%M:%S")
    current_datetime = datetime.datetime.now()
    time_remaining = race_datetime - current_datetime
    
    days_remaining = time_remaining.days
    hours_remaining = time_remaining.seconds // 3600
    minutes_remaining = (time_remaining.seconds % 3600) // 60
    seconds_remaining = time_remaining.seconds % 60
    
    countdown = {
        'days': days_remaining,
        'hours': hours_remaining,
        'minutes': minutes_remaining,
        'seconds': seconds_remaining
    }
    
    return countdown