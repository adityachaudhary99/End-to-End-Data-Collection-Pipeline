import configparser
import requests
import pandas as pd
from datetime import datetime
from datetime import timezone


def airport_codes(cities, API_key):
    icao_list = []

    url = "https://flightradar24-com.p.rapidapi.com/airports/search"

    ids_list = []
    for city in cities:
        querystring = {"q": city}

        headers = {
            "X-RapidAPI-Key": API_key,
            "X-RapidAPI-Host": "flightradar24-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        result = response.json()

        for i in result['data']:
            ids_list.append(i['id'])

    # Different API call for airport codes
    for id in ids_list:
        url = "https://flightradar24-com.p.rapidapi.com/airports/detail"

        querystring = {"airport_id": id}

        headers = {
            "X-RapidAPI-Key": API_key,
            "X-RapidAPI-Host": "flightradar24-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        result = response.json()

        if result['data']['airport']['pluginData']['details']['code']['iata'] == id:
            icao_list.append(result['data']['airport']['pluginData']['details']['code']['icao'])

    return icao_list


def flight_arrivals(icao_list, API_key):
    # Initialize an empty list to store flight data
    list_for_df = []

    # Loop over each ICAO code in the input list
    for icao in icao_list:
        params = {
            'access_key': API_key,
            'arr_icao': icao
        }

        api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

        api_response = api_result.json()

        for flight in api_response['data']:
            flight_dict = {}

            flight_dict['arrival_icao'] = icao
            flight_dict['arrival_time_local'] = datetime.fromisoformat(
            flight['arrival']['scheduled'][:-6]).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            flight_dict['arrival_terminal'] = flight['arrival']['terminal']
            flight_dict['departure_city'] = flight['departure']['timezone']
            flight_dict['departure_icao'] = flight['departure']['icao']
            flight_dict['departure_time_local'] = datetime.fromisoformat(
            flight['departure']['scheduled'][:-6]).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            flight_dict['airline'] = flight['airline']['name']
            flight_dict['flight_number'] = flight['flight']['number']
            flight_dict['data_retrieved_on'] = datetime.now().astimezone(timezone('Europe/Berlin')).date()

            list_for_df.append(flight_dict)

    # Convert the list of flight dictionaries to a DataFrame and return it
    return pd.DataFrame(list_for_df)


cities = ['Berlin', 'Hamburg', 'London']

config = configparser.ConfigParser()
config.read('config.ini')
airport_API_key = config['secret']['airport_API_key']
flight_API_key = config['secret']['flight_API_key']

airport_codes = airport_codes(cities, airport_API_key)
icao_list = airport_codes

print(icao_list)
flights_df = flight_arrivals(icao_list, flight_API_key)
print(flights_df)
