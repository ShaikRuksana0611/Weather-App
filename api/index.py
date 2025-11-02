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

    return render_template('index.html')
# Required for Vercel
app = app
