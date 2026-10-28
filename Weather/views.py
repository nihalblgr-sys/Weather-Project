import requests
from django.shortcuts import render
import os


def index(request):
    weather = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        api_key = os.environ.get("WEATHER_API_KEY")
        if not city:
            error = "Enter a city name."
        else:
            url = "https://api.weatherapi.com/v1/current.json"
            try:
                response = requests.get(
                    url,
                    params={"key": api_key, "q": city},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                if "error" in data:
                    error = data["error"].get("message", "Weather lookup failed.")
                else:
                    current = data["current"]
                    location = data["location"]
                    weather = {
                        "city": location["name"],
                        "State": location["region"],
                        "country": location["country"],
                        "date": location["localtime"],
                        "temperature": current["temp_c"],
                        "humidity": current["humidity"],
                        "wind": current["wind_kph"],
                        "condition": current["condition"]["text"],
                        "icon": current["condition"]["icon"],
                    }
            except requests.RequestException:
                error = "Unable to retrieve weather. Check your API key and connection."

    return render(request, "front.html", {"weather": weather, "error": error})
