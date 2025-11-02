from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'dc315c9afbba8e9e2f1c494d48213cc0'

def get_weather_data(city):
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            'city': city.title(),
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
    except requests.RequestException:
        return None

def get_forecast_data(city):
    try:
        url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        forecast_list = []
        for entry in data['list']:
            forecast_list.append({
                'date': entry['dt_txt'],
                'temperature': entry['main']['temp'],
                'condition': entry['weather'][0]['description']
            })
        return forecast_list
    except requests.RequestException:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    forecast = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if not city:
            error = "Please enter a city name."
        else:
            weather = get_weather_data(city)
            forecast = get_forecast_data(city)
            if weather is None:
                error = f"Could not get weather data for '{city}'. Please check the city name or try again."
    return render_template('index.html', weather=weather, forecast=forecast, error=error)

# Required for Vercel
app = app
