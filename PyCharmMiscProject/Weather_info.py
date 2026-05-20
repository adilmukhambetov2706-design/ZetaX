import requests
from datetime import datetime, timedelta
from io import BytesIO

API_KEY = "d57a3845315ffcc38df8af6af61ffb9c"
REQUEST_TIMEOUT = 3


def weather_name_from_code(code):
    if code == 0:
        return "Clear"
    if code in (1, 2, 3, 45, 48):
        return "Clouds"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "Rain"
    if code in (71, 73, 75, 77, 85, 86):
        return "Snow"
    if code in (95, 96, 99):
        return "Thunderstorm"
    return "Clouds"


class Mid_frame_info():
    def __init__(self, city="Bishkek"):
        self.city = city
        self.url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
        self.weather_data = requests.get(self.url, timeout=REQUEST_TIMEOUT).json()

    def time_right_now(self):
        timezone_offset = self.weather_data['city']['timezone']
        utc_now = datetime.utcnow()
        local_time = utc_now + timedelta(seconds=timezone_offset)
        return local_time

    def weather_today(self, i):
        return self.weather_data['list'][i]['weather'][0]['main']

    def temp_today(self, i):
        return self.weather_data['list'][i]['main']['temp']

    def wind_speed(self):
        speed_mps = self.weather_data["list"][0]["wind"]["speed"]
        return speed_mps * 3.6

    def wind_direction_degrees(self):
        if "current" in self.weather_data and "wind_dir" in self.weather_data["current"]:
            return self.wind_dir_to_degrees(self.weather_data["current"]["wind_dir"])
        return self.weather_data["list"][0]["wind"]["deg"]

    def wind_dir_to_degrees(self, wind_dir):
        directions = {
            "N": 0,
            "NNE": 22.5,
            "NE": 45,
            "ENE": 67.5,
            "E": 90,
            "ESE": 112.5,
            "SE": 135,
            "SSE": 157.5,
            "S": 180,
            "SSW": 202.5,
            "SW": 225,
            "WSW": 247.5,
            "W": 270,
            "WNW": 292.5,
            "NW": 315,
            "NNW": 337.5,
        }
        return directions.get(wind_dir.upper(), 0)

    def city_time_from_timestamp(self, timestamp):
        timezone_offset = self.weather_data["city"]["timezone"]
        return datetime.utcfromtimestamp(timestamp + timezone_offset)

    def sunrise_time(self):
        sunrise = self.weather_data["city"]["sunrise"]
        return self.city_time_from_timestamp(sunrise).strftime("%I:%M %p")

    def sunset_time(self):
        sunset = self.weather_data["city"]["sunset"]
        return self.city_time_from_timestamp(sunset).strftime("%I:%M %p")

    def air_quality(self):
        coord = self.weather_data["city"]["coord"]
        url = (
            "https://api.openweathermap.org/data/2.5/air_pollution"
            f"?lat={coord['lat']}&lon={coord['lon']}&appid={API_KEY}"
        )
        data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        return data["list"][0]["main"]["aqi"]


class Low_frame_info():
    def __init__(self, city="Bishkek"):
        self.city = city
        location = self.get_location(city)
        self.url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={location['latitude']}&longitude={location['longitude']}"
            "&daily=weather_code,temperature_2m_max,temperature_2m_min,"
            "relative_humidity_2m_mean,uv_index_max"
            "&forecast_days=14&timezone=auto"
        )
        self.weather_data = requests.get(self.url, timeout=REQUEST_TIMEOUT).json()

    def get_location(self, city):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        if "results" not in data or not data["results"]:
            raise ValueError(f"City not found: {city}")
        return data["results"][0]

    def day(self, i):
        return {
            "date": self.weather_data["daily"]["time"][i],
            "weather": self.weather_name(self.weather_data["daily"]["weather_code"][i]),
            "max_temp": self.weather_data["daily"]["temperature_2m_max"][i],
            "min_temp": self.weather_data["daily"]["temperature_2m_min"][i],
            "humidity": self.weather_data["daily"]["relative_humidity_2m_mean"][i],
            "uv": self.weather_data["daily"]["uv_index_max"][i],
        }

    def days_count(self):
        return len(self.weather_data["daily"]["time"])

    def weather_today(self, i):
        return self.day(i)["weather"]

    def max_temp(self, i):
        return self.day(i)["max_temp"]

    def min_temp(self, i):
        return self.day(i)["min_temp"]

    def date(self, i):
        return datetime.strptime(self.day(i)["date"], "%Y-%m-%d")

    def humidity(self, i):
        return self.day(i)["humidity"]

    def UV_day(self, i):
        return self.day(i)["uv"]

    def weather_name(self, code):
        return weather_name_from_code(code)


class Historical_day_info:
    def __init__(self, city, selected_date):
        self.city = city
        self.selected_date = selected_date
        location = self.get_location(city)
        self.url = (
            "https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={location['latitude']}&longitude={location['longitude']}"
            f"&start_date={selected_date}&end_date={selected_date}"
            "&daily=weather_code,temperature_2m_max,temperature_2m_min,"
            "relative_humidity_2m_mean,uv_index_max,sunrise,sunset"
            "&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            "&timezone=auto"
        )
        self.weather_data = requests.get(self.url, timeout=REQUEST_TIMEOUT).json()

    def get_location(self, city):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        if "results" not in data or not data["results"]:
            raise ValueError(f"City not found: {city}")
        return data["results"][0]

    def daily(self):
        return self.weather_data["daily"]

    def hourly(self):
        return self.weather_data["hourly"]

    def weather(self):
        code = self.daily()["weather_code"][0]
        return weather_name_from_code(code)

    def max_temp(self):
        return self.daily()["temperature_2m_max"][0]

    def min_temp(self):
        return self.daily()["temperature_2m_min"][0]

    def humidity(self):
        return self.daily()["relative_humidity_2m_mean"][0]

    def uv(self):
        return self.daily()["uv_index_max"][0]

    def sunrise_time(self):
        return datetime.fromisoformat(self.daily()["sunrise"][0]).strftime("%I:%M %p")

    def sunset_time(self):
        return datetime.fromisoformat(self.daily()["sunset"][0]).strftime("%I:%M %p")

    def hourly_time(self, i):
        return datetime.fromisoformat(self.hourly()["time"][i]).strftime("%H:%M")

    def hourly_temp(self, i):
        return self.hourly()["temperature_2m"][i]

    def hourly_wind(self, i):
        return self.hourly()["wind_speed_10m"][i]

    def hourly_weather(self, i):
        code = self.hourly()["weather_code"][i]
        return weather_name_from_code(code)


class Trd_page_info:
    def __init__(self, city):
        self.city = city
        self.url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
        self.weather_data = requests.get(self.url, timeout=REQUEST_TIMEOUT).json()
        self.country_code = None

    def temp(self):
        return self.weather_data['list'][0]['main']['temp']

    def icon(self):
        icons =  self.weather_data['list'][0]['weather'][0]['icon']
        response = requests.get(f"https://openweathermap.org/img/wn/{icons}@2x.png", timeout=REQUEST_TIMEOUT)
        return BytesIO(response.content)

    def time(self):
        timezone_offset = self.weather_data['city']['timezone']
        utc_now = datetime.utcnow()
        return utc_now + timedelta(seconds=timezone_offset)

    def country(self):
        if self.country_code:
            return self.country_code

        response = requests.get(
            f"https://nominatim.openstreetmap.org/search?city={self.city}&format=json&addressdetails=1",
            headers={"User-Agent": "my-app"},
            timeout=REQUEST_TIMEOUT).json()
        self.country_code = response[0]["address"]["country_code"]
        return self.country_code

    def flag(self):
        country_code = self.country()
        response = requests.get(f"https://flagsapi.com/{country_code.upper()}/flat/64.png", timeout=REQUEST_TIMEOUT)
        img_data = BytesIO(response.content)
        return img_data
