import requests

def get_weather(city="Kollam"):
    API_KEY = "47aca9cff4865608a4266e16cbccf60c"  # ← replace this
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather_main = data["weather"][0]["main"]  # Rain, Clear, Clouds etc.
            is_rainy = 1 if weather_main in ["Rain", "Drizzle", "Thunderstorm"] else 0

            return {
                "temperature": round(temp, 1),
                "is_rainy": is_rainy,
                "weather_description": weather_main
            }
        else:
            print(f"Weather API error: {data.get('message', 'Unknown error')}")
            return {"temperature": 30.0, "is_rainy": 0, "weather_description": "Clear"}

    except Exception as e:
        print(f"Could not fetch weather: {e}")
        return {"temperature": 30.0, "is_rainy": 0, "weather_description": "Clear"}


# Test it
if __name__ == "__main__":
    weather = get_weather("Kollam")
    print(weather)