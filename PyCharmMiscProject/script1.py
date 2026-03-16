from customtkinter import *
from PIL import Image
import requests
from random import randint
from datetime import datetime, timedelta

#API_KEY = "d57a3845315ffcc38df8af6af61ffb9c"

#city = "Bishkek"

#url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"

#data = requests.get(url).json()


weather = weather_data['list'][0]['weather'][0]['description']

print(weather)
