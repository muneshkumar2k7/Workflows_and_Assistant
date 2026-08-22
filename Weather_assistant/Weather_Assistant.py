from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from typing import Literal 
import os
import requests
from datetime import datetime, timedelta

loaded = load_dotenv()




llms = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)



class Loc_Request(BaseModel):
    city: str | None = None
 


class Time_Request(BaseModel):
      time: Literal[
           "today",
           "future",
           "past"
       ] = "today"
      days: int | None = None

Loc_structured_llm = llms.with_structured_output(Loc_Request)
Time_structured_llm = llms.with_structured_output(Time_Request)

loc_query_template = ChatPromptTemplate.from_template("""

 Extract the city name from the user query if exists, otherwise return none.

User Question:
{query}
"""
)

time_query_template = ChatPromptTemplate.from_template(
"""
You are a weather assistant. Extract the time information from the user query.

Rules:

1. Return time = "today" when the user asks about:
   - current weather
   - now
   - today
   - present weather
   - weather without any specific time

2. Return time = "future" when the user asks about:
   - tomorrow
   - next day
   - upcoming days
   - next week
   - future weather
   - forecast

   Extract the number of days if mentioned:
   - "next 3 days" -> days = 3
   - "next 7 days" -> days = 7
   - "tomorrow" -> days = 1

3. Return time = "past" when the user asks about:
   - yesterday
   - previous days
   - last week
   - historical weather

   Extract the number of days if mentioned:
   - "last 3 days" -> days = 3
   - "last 7 days" -> days = 7
   - "yesterday" -> days = 1


If no number of days is mentioned:
return days = None.


User Query:
{query}

Return only the structured output.
"""
)

weather_query_template = ChatPromptTemplate.from_template(
"""
   User Question:
   {query}

Weather Data:
data = {weather_data}

Instructions:
Answer using only the provided weather information.

"""

)
print("Current Directory:", os.getcwd())

def get_current_city():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    return data["city"]



def get_weather(city:str, time_frame: str , days: int | None = None):
    """
    Get the weather information for a given city and time frame.
    """

    if city is None:
      city = get_current_city()
     
    api_key = os.getenv("OPEN_MAP_WEATHER")
    geo_url = "https://api.openweathermap.org/geo/1.0/direct"
  
    geo_params = {
        "q":city,
        "limit" :1,
        "appid":api_key

    }


    geo_response = requests.get(url=geo_url, params=geo_params)
  

    geo_data = geo_response.json()
    
    if not geo_data:
     return "City not found"

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    
    if time_frame == "today":
     weather_url = "https://api.openweathermap.org/data/2.5/weather"
     weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
     }  

     weather_response = requests.get(
        weather_url,
        params=weather_params
    )

     weather_data = weather_response.json()
     return weather_data

    elif time_frame  == "future":
       weather_url = "https://api.open-meteo.com/v1/forecast"
       params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min",
            "forecast_days": days if days is not None else 7,
            "timezone": "auto"
}
       weather_response = requests.get(
        weather_url,
        params=params
    )       
       weather_data = weather_response.json()
       return weather_data
    
    elif time_frame == "past":
       weather_url = "https://archive-api.open-meteo.com/v1/archive"
       end_date = datetime.now()
       start_date = end_date - timedelta(days=days if days is not None else 7)

       params = {
           "latitude": lat,
           "longitude": lon,
           "start_date": start_date.strftime("%Y-%m-%d"),
           "end_date": end_date.strftime("%Y-%m-%d"),
           "daily": "weather_code,temperature_2m_max,temperature_2m_min",
           "timezone": "auto"
       }


       weather_response = requests.get(
        weather_url,
        params=params
    )       
       weather_data = weather_response.json()
       return weather_data
    









while True:

    query  = input("Enter the City or (q to quit)")

    
    if query.lower()  == 'q':
        break


    loc_query = loc_query_template.invoke({"query": query})
    loc_response = Loc_structured_llm.invoke(loc_query)
    time_query = time_query_template.invoke({"query": query})
    time_response = Time_structured_llm.invoke(time_query)

    city_name = loc_response.city
    time_frame = time_response.time
    days = time_response.days

    result = get_weather(city_name, time_frame, days)
    prompt = weather_query_template.invoke({"query": query, "weather_data": result})
    ans = llms.invoke(prompt)
    print("\nAI Message:", ans.content)
      
