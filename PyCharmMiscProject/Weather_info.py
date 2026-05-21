import requests
from datetime import datetime, timedelta, timezone
from io import BytesIO
import time

API_KEY = "d57a3845315ffcc38df8af6af61ffb9c"
REQUEST_TIMEOUT = 3
CACHE_TTL = 60

_location_cache = {}
_mid_frame_cache = {}
_low_frame_cache = {}
_historical_cache = {}


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


def _get_location(city):
    if city in _location_cache:
        return _location_cache[city]
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
    if "results" not in data or not data["results"]:
        raise ValueError(f"City not found: {city}")
    _location_cache[city] = data["results"][0]
    return _location_cache[city]


class Mid_frame_info():
    def __init__(self, city="Bishkek"):
        self.city = city
        cached = _mid_frame_cache.get(city)
        if cached and time.monotonic() - cached[1] < CACHE_TTL:
            self.weather_data = cached[0]
            return
        self.url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
        self.weather_data = requests.get(self.url, timeout=REQUEST_TIMEOUT).json()
        _mid_frame_cache[city] = (self.weather_data, time.monotonic())

    def time_right_now(self):
        timezone_offset = self.weather_data['city']['timezone']
        return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=timezone_offset)

    def weather_today(self, i):
        return self.weather_data['list'][i]['weather'][0]['main']

    def temp_today(self, i):
        return self.weather_data['list'][i]['main']['temp']

    def wind_speed(self):
        speed_mps = self.weather_data["list"][0]["wind"]["speed"]
        return speed_mps * 3.6

    def wind_direction_degrees(self):
        return self.weather_data["list"][0]["wind"]["deg"]

    def city_time_from_timestamp(self, timestamp):
        timezone_offset = self.weather_data["city"]["timezone"]
        return datetime.fromtimestamp(timestamp + timezone_offset, tz=timezone.utc).replace(tzinfo=None)

    def sunrise_time(self):
        sunrise = self.weather_data["city"]["sunrise"]
        return self.city_time_from_timestamp(sunrise).strftime("%I:%M %p")

    def sunset_time(self):
        sunset = self.weather_data["city"]["sunset"]
        return self.city_time_from_timestamp(sunset).strftime("%I:%M %p")

    def air_quality(self):
        if hasattr(self, '_aqi'):
            return self._aqi
        coord = self.weather_data["city"]["coord"]
        url = (
            "https://api.openweathermap.org/data/2.5/air_pollution"
            f"?lat={coord['lat']}&lon={coord['lon']}&appid={API_KEY}"
        )
        data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        self._aqi = data["list"][0]["main"]["aqi"]
        return self._aqi


class Low_frame_info():
    def __init__(self, city="Bishkek"):
        self.city = city
        cached = _low_frame_cache.get(city)
        if cached and time.monotonic() - cached[1] < CACHE_TTL:
            self.weather_data = cached[0]
            return
        location = _get_location(city)
        self.url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={location['latitude']}&longitude={location['longitude']}"
            "&daily=weather_code,temperature_2m_max,temperature_2m_min,"
            "relative_humidity_2m_mean,uv_index_max"
            "&forecast_days=14&timezone=auto"
        )
        self.weather_data = requests.get(self.url, timeout=REQUEST_TIMEOUT).json()
        _low_frame_cache[city] = (self.weather_data, time.monotonic())

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
        cache_key = (city, selected_date)
        if cache_key in _historical_cache:
            self.weather_data = _historical_cache[cache_key]
            return
        location = _get_location(city)
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
        _historical_cache[cache_key] = self.weather_data

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

    def temp(self):
        return self.weather_data['list'][0]['main']['temp']

    def icon(self):
        icons = self.weather_data['list'][0]['weather'][0]['icon']
        response = requests.get(f"https://openweathermap.org/img/wn/{icons}@2x.png", timeout=REQUEST_TIMEOUT)
        return BytesIO(response.content)

    def time(self):
        timezone_offset = self.weather_data['city']['timezone']
        return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=timezone_offset)

    def country(self):
        return self.weather_data['city']['country']

    def flag(self):
        country_code = self.country()
        response = requests.get(f"https://flagsapi.com/{country_code.upper()}/flat/64.png", timeout=REQUEST_TIMEOUT)
        return BytesIO(response.content)
