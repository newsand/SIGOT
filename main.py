from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel

from gemini_connector import GeminiConnector
from openwhater_connector import get_weather_data_asc

# Define the API function
app = FastAPI()

class WeatherRequest(BaseModel):
    city: str
    country: str
    lang: str

# Function to get weather data from OpenWeatherAPI
connector = GeminiConnector(model_name="gemini-1.5-flash")
@app.get("/")
async def root():
    return {"message": "Hello World"}
#
@app.post("/shouldI")
async def should_i(weather_request: WeatherRequest):
    try:
        weather_data = await get_weather_data_asc(weather_request.city, weather_request.country)
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        rain = weather_data['rain']['3h'] if 'rain' in weather_data else 0
        wind = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description']
    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(content={"message": "Something went wrong. Please try again later."}, status_code=500)
    prompt = (f"Should I go outside today? The weather is {description}, \
              and the temperature feels like {feels_like:.1f}°C.,\
              and the wind speed is {wind:.1f}, \
              and raining chance / hour is {rain:.1f},\
              and the humidity is {humidity:.1f}°C.\
              answer in {weather_request.lang}")
    print(prompt)
    gemni_response = await connector.send_prompt_asc(prompt)
    return gemni_response
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)