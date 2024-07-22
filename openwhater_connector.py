import aiohttp
import requests
import asyncio
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from requests import RequestException

load_dotenv()
OPENWEATHERAPI_KEY = os.getenv("OPENWEATHERAPI_KEY")
# Function to get weather data from OpenWeatherAPI
def get_weather_data(city: str, country: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={OPENWEATHERAPI_KEY}"
    response =  requests.get(url=url)
    # Handle error if city or country is not found
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City or country not found")

    return response.json()

async def get_weather_data_asc(city: str, country: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid={OPENWEATHERAPI_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status!=200:
                raise ValueError("city or country not found")
            return await response.json()


# Create and run the event loop
async def main():
    try:
        weather_data = await get_weather_data_asc("Belo Horizonte", "Brazil")
        print(weather_data)
    except ValueError as e:
        print(f"Error: {e}")
    except RequestException as e:
        print(f"Network Error: {e}")

if __name__ == "__main__":

    #weather_data = get_weather_data("Belo Horizonte", "Brazil")
    asyncio.run(main())
