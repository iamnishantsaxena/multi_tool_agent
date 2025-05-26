import requests
from geopy.geocoders import Nominatim
from pydantic import BaseModel, validator
from typing import Optional


class WeatherData(BaseModel):
  temperature_2m: float
  relative_humidity_2m: int
  rain: float
  weather_code: int


class CurrentWeather(BaseModel):
  current: WeatherData


class WeatherReport(BaseModel):
  status: str
  report: Optional[str] = None
  error_message: Optional[str] = None


  @validator("status")
  def status_must_be_valid(cls, v):
    if v not in ["success", "error"]:
      raise ValueError("Status must be 'success' or 'error'")
    return v


def get_weather(city: str) -> WeatherReport:
  """Retrieves the current weather report for a specified city using the Open-Meteo API.

  Args:
    city (str): The name of the city for which to retrieve the weather report.

  Returns:
    WeatherReport: A WeatherReport object containing the weather report or an error message.
  """
  try:
    latitude, longitude = _get_city_coordinates(city)
    weather_data = _fetch_weather_data(latitude, longitude)
    parsed_data = CurrentWeather(**weather_data)
    report = _parse_weather_data(parsed_data, city)

    return WeatherReport(status="success", report=report)

  except requests.exceptions.RequestException as e:
    return WeatherReport(status="error", error_message=f"Error fetching weather data: {e}")
  except (KeyError, TypeError, ValueError) as e:
    return WeatherReport(status="error", error_message=f"Error parsing weather data: {e}")
  except Exception as e:
    return WeatherReport(status="error", error_message=f"Error finding coordinates: {e}")


def _get_city_coordinates(city: str) -> tuple[float, float]:
  """Retrieves the coordinates of a city using geopy.

  Args:
    city (str): The name of the city.

  Returns:
    tuple[float, float]: The latitude and longitude of the city.
  """
  geolocator = Nominatim(user_agent="weather_app")
  location = geolocator.geocode(city)

  if location is None:
    raise ValueError(f"Could not find coordinates for {city}")

  latitude = location.latitude
  longitude = location.longitude
  return latitude, longitude


def _fetch_weather_data(latitude: float, longitude: float) -> dict:
  """Fetches weather data from the Open-Meteo API.

  Args:
    latitude (float): The latitude of the city.
    longitude (float): The longitude of the city.

  Returns:
    dict: The weather data in JSON format.
  """
  url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,rain,weather_code"
  response = requests.get(url)
  response.raise_for_status()
  return response.json()


def _parse_weather_data(weather_data: CurrentWeather, city: str) -> str:
  """Parses the weather data and returns a human-readable report.

  Args:
    weather_data (CurrentWeather): The weather data.
    city (str): The name of the city.

  Returns:
    str: A human-readable weather report.
  """
  temperature = weather_data.current.temperature_2m
  humidity = weather_data.current.relative_humidity_2m
  rain = weather_data.current.rain
  weather_code = weather_data.current.weather_code

  weather_description = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight intensity",
    81: "Rain showers: Moderate intensity",
    82: "Rain showers: Violent intensity",
    85: "Snow showers slight",
    86: "Snow showers heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
  }.get(weather_code, "Unknown")

  report = (
    f"The current weather in {city.capitalize()} is: {weather_description}, "
    f"Temperature: {temperature}°C, "
    f"Relative Humidity: {humidity}%, "
    f"Rain: {rain} mm"
  )
  return report
