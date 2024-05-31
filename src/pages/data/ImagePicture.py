import requests
from io import BytesIO
from PIL import Image
import datetime

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

team_year = 2024
    
def get_team_profile_picture(team):
    
    # Construct the profile picture URL based on the driver's name
    profile_picture_url = f"https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/{team_year}/{team_name[team]}"

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