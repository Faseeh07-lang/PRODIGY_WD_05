from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime,timedelta
from django.views.generic import TemplateView

api_key='5662574cb0f90f2b4ada31129c5d70ff'

@api_view(['GET', 'POST'])
def get_weather(request):
    if request.method == "POST":
        city = request.POST.get("city_name")
    else:
        city = "New York"
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        contexts = {
            'temperature': weather_data.get("main", {}).get("temp"),
            'pressure': weather_data.get("main", {}).get("pressure"),
            'humidity': weather_data.get("main", {}).get("humidity"),
            "wind": weather_data.get("wind", {}).get("speed"),
            'weather': weather_data.get('weather', [{}])[0].get('main'),
            'weather_icon': weather_data.get('weather', [{}])[0].get('icon'),
            "city": weather_data.get("name")
        }
    
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    forecast_response = requests.get(forecast_url)
    seven_day_data = forecast_response.json()
    forecast_data = []
    
    current_day = datetime.now()
    days_list = [(current_day + timedelta(days=i)).strftime("%A") for i in range(7)]
    
    if forecast_response.status_code == 200:
        for i, item in enumerate(seven_day_data.get("list", [])):
            if i % 8 == 0:  # OpenWeather returns data every 3 hours, so pick every 8th to get daily data
                date_time = datetime.fromtimestamp(item.get("dt"))
                date = date_time.strftime("%Y-%m-%d")
                daily_data = {
                    "day_name": days_list[i // 8],
                    "date": date,
                    "pressure": item.get("main", {}).get("pressure"),
                    "humidity": item.get("main", {}).get("humidity"),
                    "temp": item.get("main", {}).get("temp"),
                    "weather": item.get("weather", [{}])[0].get("main"),
                    "description": item.get("weather", [{}])[0].get("description"),
                    "icon": item.get("weather", [{}])[0].get("icon"),
                    "wind": item.get("wind", {}).get("speed"),
                }
                forecast_data.append(daily_data)
        
        context = {
            "current_day": contexts,
            "forecast": forecast_data,
            "current_day_name": days_list[0],
        }
    else:
        context = {"error": "The data did not get fetched"}
    
    return render(request, "index.html", context)

class Home_view(TemplateView):
      template_name="home.html"
class Contact_view(TemplateView):
    template_name="contact.html"

    

    
    

