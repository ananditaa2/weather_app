import streamlit as st
import asyncio
import aiohttp
import os

# reuse your existing logic!
class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, city):
        params = {'q': city, 'appid': self.api_key, 'units': 'metric'}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=params) as resp:
                return await resp.json()

# Streamlit UI
st.title("🌤️ My Weather Web App")
city = st.text_input("Enter City Name", "Raipur")

if st.button("Check Weather"):
    service = WeatherService(os.getenv("WEATHER_API_KEY", "94716215fcb180af30452411e90ab8c7"))
    data = asyncio.run(service.get_weather(city))
    
    if data.get("cod") == 200:
        st.metric("Temperature", f"{data['main']['temp']}°C")
        st.write(f"Condition: {data['weather'][0]['description'].capitalize()}")
    else:
        st.error("City not found!")