import requests
from io import BytesIO
from PIL import Image
import datetime
from bs4 import BeautifulSoup
import datetime

team_name = {
    "Red Bull Racing Honda RBPT": "red-bull-racing",
    "Ferrari": "ferrari",
    "McLaren Mercedes": "mclaren",
    "Mercedes": "mercedes",
    "Aston Martin Aramco Mercedes": "aston-martin",
    "RB Honda RBPT": "rb",
    "Haas Ferrari": "haas",
    "Williams Mercedes": "williams",
    "Alpine Renault": "alpine",
    "Kick Sauber Ferrari": "kick-sauber",
}


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

def get_driver_profile_picture(driver_name, year = None, stop = False):
    if year is None:
        year = datetime.datetime.now().year
        
    name = driver_name.split(" ")[1].lower()
    
    # Construct the profile picture URL based on the driver's name
    profile_picture_url = f"https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/drivers/{year}Drivers/{name}"

    print(profile_picture_url)

    # Append the file extension
    profile_picture_url += ".jpg"

    # Send a GET request to download the image
    response = requests.get(profile_picture_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open the image from the response content
        image = Image.open(BytesIO(response.content))
        return image
    elif not stop:
        return get_driver_profile_picture(driver_name, year - 1, True)
    else:
        return None
    
def get_team_profile_picture(team):
    
    # Construct the profile picture URL based on the driver's name
    profile_picture_url = f"https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/{datetime.datetime.now().year}/{team_name[team]}"

    print(profile_picture_url)

    # Append the file extension
    profile_picture_url += ".png"

    # Send a GET request to download the image
    response = requests.get(profile_picture_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open the image from the response content
        image = Image.open(BytesIO(response.content))
        return image
    else:
        return None