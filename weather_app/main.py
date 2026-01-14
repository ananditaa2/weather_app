import asyncio  # Theory: The 'manager' for async tasks
import aiohttp  # Theory: An async-friendly library to make web requests
import os       # Theory: To interact with your computer's OS (to get the API key)
import json     # Theory: To turn the text from the API into a Python Dictionary

# --- OOP: We wrap everything in a Class ---
class WeatherService:
    def __init__(self, api_key):
        """OOP Theory: This 'Constructor' sets up the object's brain."""
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def fetch_data(self, city):
        """Async Theory: 'async' tells Python this function can 'wait' without freezing."""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }

        # --- Error Handling: try/except prevents the app from crashing ---
        try:
            async with aiohttp.ClientSession() as session:
                # 'await' tells the code: "Pause here until the website responds"
                async with session.get(self.base_url, params=params) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        self.display_report(data)
                    elif response.status == 401:
                        print("❌ Error: API Key is invalid or not yet active. Wait 30 mins!")
                    else:
                        print(f"❌ Error: City not found (Status {response.status})")
        
        except aiohttp.ClientConnectorError:
            print("🌐 Error: Check your internet connection.")
        except Exception as e:
            print(f"⚠️ An unexpected error occurred: {e}")

    def display_report(self, data):
        """Theory: Parsing JSON. We dig into the dictionary to find info."""
        city = data.get("name")
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        
        print("-" * 30)
        print(f"📍 City: {city}")
        print(f"🌡️  Temp: {temp}°C")
        print(f"☁️  Sky:  {weather.capitalize()}")
        print("-" * 30)

# --- The 'Entry Point' ---
async def main():
    # Use 'os' to get that key you 'set' in the terminal earlier
    key = os.getenv("WEATHER_API_KEY")
    
    if not key:
        print("❌ API Key not found!")
        print("To fix this, set the environment variable in your terminal:")
        print("  PowerShell: $env:WEATHER_API_KEY = 'your_api_key'")
        print("  CMD:        set WEATHER_API_KEY=your_api_key")
        print("  Bash/Zsh:   export WEATHER_API_KEY=your_api_key")
        return

    # OOP: Create an 'instance' of our class
    weather_app = WeatherService(key)
    
    city_name = input("Enter city name: ").strip()
    if city_name:
        await weather_app.fetch_data(city_name)

if __name__ == "__main__":
    # Start the async loop
    asyncio.run(main())