import requests
from bs4 import BeautifulSoup
import datetime

def get_driver_standings(year = None):
    
    if(year == None):
        year = datetime.datetime.now().year
    
    
    url = f"https://www.formula1.com/en/results.html/{year}/drivers.html"  # URL for driver standings
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    standings = []
    table = soup.find('table', class_='resultsarchive-table')
    rows = table.find('tbody').find_all('tr')

    for row in rows:
        columns = row.find_all('td')
        position = columns[1].text.strip()
        name = columns[2].text.strip().replace('\n', ' ')[:-4]
        team = columns[4].text.strip()
        points = columns[5].text.strip()

        standings.append({
            'position': position,
            'name': name,
            'team': team,
            'points': points
        })

    if(standings == []):
        return get_driver_standings(year - 1)
    
    return standings

def get_team_standings(year = None):
    
    if(year == None):
        year = datetime.datetime.now().year
    
    url = f"https://www.formula1.com/en/results.html/{year}/team.html"  # URL for driver standings
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    standings = []
    table = soup.find('table', class_='resultsarchive-table')
    rows = table.find('tbody').find_all('tr')

    for row in rows:
        columns = row.find_all('td')
        position = columns[1].text.strip()
        team = columns[2].text.strip()
        points = columns[3].text.strip()

        standings.append({
            'position': position,
            'team': team,
            'points': points,
        })

    if(standings == []):
        return get_team_standings(year - 1)
    
    return standings