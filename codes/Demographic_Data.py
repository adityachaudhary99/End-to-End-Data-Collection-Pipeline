# Import the libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd


def wiki_scrape(cities):
    info_list = []

    for city in cities:
        url = f"https://en.wikipedia.org/wiki/{city}"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        response_dict = {'city': soup.select('#firstHeading')[0].get_text(),
                         'country': soup.select('.infobox-data')[0].get_text(),
                         'latitude': soup.select('.latitude')[0].get_text(),
                         'longitude': soup.select('.longitude')[0].get_text()}

        if soup.select_one('.infobox-label:-soup-contains("Elevation")'):
            response_dict['elevation'] = soup.select_one('.infobox-label:-soup-contains("Elevation")').find_next(
                class_='infobox-data').get_text()
            response_dict['website'] = soup.select_one('.infobox-label:-soup-contains("Website")').find_next(
                class_='infobox-data').get_text()

        if soup.select_one('.infobox-label:-soup-contains("Population")'):
            response_dict['population'] = soup.select_one('.infobox-label:-soup-contains("Population")').find_next(
                class_='infobox-data').get_text()

        info_list.append(response_dict)

    cities_info = pd.DataFrame(info_list)

    return cities_info


cities = ['Berlin', 'Hamburg', 'London']
cities_df = wiki_scrape(cities)
print(cities_df)
