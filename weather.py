import requests
from config import WEATHER_API_KEY

print("Weather Key:", WEATHER_API_KEY)
def get_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if str(data.get("cod")) != "200":

            return None

        return {
            "city": data["name"],
            "temp": round(data["main"]["temp"]),
            "condition": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind": round(data["wind"]["speed"] * 3.6)
        }

    except Exception as e:

        print("Weather Error:", e)

        return None