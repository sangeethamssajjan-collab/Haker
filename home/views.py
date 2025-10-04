from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    return render(request, 'index.html')

def nameRef(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if not name:
            return HttpResponse("Please enter your name.")
        
        name1 = name.lower()
        
        if "script" in name1:
            # Replace "script" with empty string
            name2 = name1.replace("script", "")
            return HttpResponse(name2)
        else:
            return HttpResponse(name1)
    else:
        return HttpResponse("Please enter your name.")


def weather(request):
    city = request.GET.get('city', 'Bengaluru')  # default city
    api_key = "6344ec104463b40b9efb633d0171bfb1"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and "main" in data:
        from datetime import datetime
        def format_time(ts):
            try:
                return datetime.fromtimestamp(ts).strftime('%H:%M')
            except:
                return '-'
        weather_data = {
            "city": data.get("name", city),
            "temperature": data["main"].get("temp"),
            "feels_like": data["main"].get("feels_like"),
            "temp_min": data["main"].get("temp_min"),
            "temp_max": data["main"].get("temp_max"),
            "humidity": data["main"].get("humidity"),
            "pressure": data["main"].get("pressure"),
            "description": data["weather"][0]["description"].title() if data.get("weather") else '-',
            "icon": data["weather"][0]["icon"] if data.get("weather") else '',
            "wind_speed": data["wind"].get("speed") if data.get("wind") else '-',
            "clouds": data["clouds"].get("all") if data.get("clouds") else '-',
            "country": data["sys"].get("country") if data.get("sys") else '-',
            "sunrise": format_time(data["sys"].get("sunrise")) if data.get("sys") else '-',
            "sunset": format_time(data["sys"].get("sunset")) if data.get("sys") else '-',
        }
    else:
        weather_data = {"error": "City not found"}
    return render(request, "weather/index.html", {"weather": weather_data})
