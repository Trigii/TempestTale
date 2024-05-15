import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

BASE_URL = "https://www.tiempo3.com/europe/spain"

MONTHS= ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

FILEPATH = "tempestdb.json"

class City():
    def __init__(self, name, url, onUse=False):
        self.name = name
        self.url = url
        self.onUse = onUse

class TempestDB():
    def __init__(self):
        self.numCities = 0
        self.citiesInUse = 0
        self.cities = {}

        # Compute current month
        current_month = datetime.now().month
        self.month = MONTHS[current_month - 1]

        timezone = timedelta(hours=1)
        tomorrow = datetime.now() + timedelta(days=1)
        self.notValidAfter = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0) + timezone

    def addCity(self, city):
        self.cities[city.name] = city
        self.numCities += 1

    def useCity(self, cityName):
        self.cities[cityName].onUse = True
        self.citiesInUse += 1

    def hasCity(self, city):
        return city in self.cities.keys()

    def getCityURL(self, cityName):
        for city in self.cities.values():
            if city.name == cityName:
                return city.url
        return None

    def loadCities(self):
        response = requests.get(BASE_URL + "?page=month&month=" + self.month)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        for option in soup.find_all('option'):
            city_name = option.text.strip()
            city_url = option['value']

            self.addCity(City(city_name, city_url))

    def saveInFile(self):
        data = {
            'notValidAfter': str(self.notValidAfter),
            'month': self.month,
            'numCities': self.numCities,
            'citiesInUse': self.citiesInUse,
            'cities': [city.__dict__ for city in self.cities.values()]
        }
        with open(FILEPATH, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def loadFromFile():
        try:
            with open(FILEPATH, 'r') as file:
                data = json.load(file)

            tempestDb = TempestDB()
            tempestDb.notValidAfter = datetime.fromisoformat(data['notValidAfter'])
            tempestDb.numCities = 0
            tempestDb.citiesInUse = data['citiesInUse']

            for city_data in data['cities']:
                city = City(city_data['name'], city_data['url'], city_data['onUse'])
                tempestDb.addCity(city)

            return tempestDb
        except:
            return None

    def displayStatus(self):
        print("Month: {}".format(self.month))
        print("Total cities: {}".format(self.numCities))
        print("Cities in use: {}/{}".format(self.citiesInUse, self.numCities))

        for city in self.cities.values():
            if city.onUse:
                print("\tCity: {}".format(city.name))