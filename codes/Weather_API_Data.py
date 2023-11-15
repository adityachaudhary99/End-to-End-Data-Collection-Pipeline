import pandas as pd
import requests
import configparser
from datetime import datetime


def weather_data(cities, API_key):

    weather_dict = {'city': [],
                    'country': [],
                    'forecast_time': [],
                    'outlook': [],
                    'detailed_outlook': [],
                    'temperature': [],
                    'temperature_feels_like': [],
                    'clouds': [],
                    'rain': [],
                    'snow': [],
                    'wind_speed': [],
                    'wind_deg': [],
                    'humidity': [],
                    'pressure': [],
                    'information_retrieved_at': []}

    for city in cities:
        now = datetime.now().astimezone()

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_key}&units=metric"

        response = requests.get(url)
        result = response.json()

        for i in result['list']:
            weather_dict['city'].append(result['city']['name'])
            weather_dict['country'].append(result['city']['country'])
            weather_dict['forecast_time'].append(i['dt_txt'])
            weather_dict['outlook'].append(i['weather'][0]['main'])
            weather_dict['detailed_outlook'].append(i['weather'][0]['description'])
            weather_dict['temperature'].append(i['main']['temp'])
            weather_dict['temperature_feels_like'].append(i['main']['feels_like'])
            weather_dict['clouds'].append(i['clouds']['all'])

            try:
                weather_dict['rain'].append(i['rain']['3h'])
            except:
                weather_dict['rain'].append('0')
            try:
                weather_dict['snow'].append(i['snow']['3h'])
            except:
                weather_dict['snow'].append('0')

                weather_dict['wind_speed'].append(i['wind']['speed'])
                weather_dict['wind_deg'].append(i['wind']['deg'])
                weather_dict['humidity'].append(i['main']['humidity'])
                weather_dict['pressure'].append(i['main']['pressure'])
                weather_dict['information_retrieved_at'].append(now.strftime("%d/%m/%Y %H:%M:%S"))

    return pd.DataFrame(weather_dict)


config = configparser.ConfigParser()
config.read('config.ini')
API_key = config['secret']['API_key']

cities = ['Berlin', 'Hamburg', 'London']
print(weather_data(cities, API_key))




