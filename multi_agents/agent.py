from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search

import requests

from google.adk.tools import google_search
from geopy.geocoders import Nominatim

def get_weather(city: str) -> dict:
  """Retrieves the current weather report for a specified city using the Open-Meteo API.

  Args:
    city (str): The name of the city for which to retrieve the weather report.

  Returns:
    dict: A dictionary containing the weather report or an error message.
  """
  try:
    latitude, longitude = _get_city_coordinates(city)
    weather_data = _fetch_weather_data(latitude, longitude)
    report = _parse_weather_data(weather_data, city)

    return {"status": "success", "report": report}

  except requests.exceptions.RequestException as e:
    return {"status": "error", "error_message": f"Error fetching weather data: {e}"}
  except (KeyError, TypeError) as e:
    return {"status": "error", "error_message": f"Error parsing weather data: {e}"}
  except Exception as e:
    return {"status": "error", "error_message": f"Error finding coordinates: {e}"}


def _get_city_coordinates(city: str) -> tuple[float, float]:
  """Retrieves the coordinates of a city using google_search.

  Args:
    city (str): The name of the city.

  Returns:
    tuple[float, float]: The latitude and longitude of the city.
  """
  # Use a more reliable geocoding service like geopy instead of google_search

  geolocator = Nominatim(user_agent="weather_app")  # Replace "weather_app" with a descriptive name
  location = geolocator.geocode(city)

  if location is None:
    raise ValueError(f"Could not find coordinates for {city}")

  latitude = location.latitude
  longitude = location.longitude
  return latitude, longitude
  latitude = float(search_result.split("Latitude: ")[1].split(",")[0].strip())
  longitude = float(search_result.split("Longitude: ")[1].split(",")[0].strip())
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
  response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
  return response.json()


def _parse_weather_data(weather_data: dict, city: str) -> str:
  """Parses the weather data and returns a human-readable report.

  Args:
    weather_data (dict): The weather data in JSON format.
    city (str): The name of the city.

  Returns:
    str: A human-readable weather report.
  """
  temperature = weather_data["current"]["temperature_2m"]
  humidity = weather_data["current"]["relative_humidity_2m"]
  rain = weather_data["current"]["rain"]
  weather_code = weather_data["current"]["weather_code"]

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

import datetime
from zoneinfo import ZoneInfo

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}
  
# from weather_util import get_weather
# from time_util import get_current_time

# Create an instance of the LlmAgent for Weather and Time
weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash-exp",
    description=(
      "Agent to answer questions about the weather and time in a city."
    ),
    instruction=(
      "You are a helpful agent who can answer user questions about the weather and time in a city."
    ),
    tools=[get_weather, get_current_time],
)

search_agent = Agent(
    model="gemini-2.0-flash-exp", # Required: Specify the LLM 
    name="question_answer_agent", # Required: Unique agent name
    description="A helpful assistant agent that can answer questions.",
    instruction="""Respond to the query using google search""",
    tools=[google_search], # Provide an instance of the tool
)

# Create an instance of the LlmAgent for the root agent
root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash-exp",
    description=(
      "Agent to delegate tasks to other agents based on user queries."
    ),
    instruction=(
      "You are a helpful agent who can delegate user queries to other agents. "
      "If the user asks about the weather or time, delegate the task to the weather agent. "
      "If the user asks to search for something, delegate the task to the search agent."
    ),
    sub_agents=[search_agent, weather_agent],
)