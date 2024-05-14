import json
import requests
from bs4 import BeautifulSoup

CITIES_PATH = "cities/"

BLOCK_SIZE = 16

class CityData():
    def __init__(self,
                 name = None,
                 url = None,
                 hasEncKey = False,
                 encKey = "",
                 html = None,
                 status = None,
                 totalCapacity = 0,
                 realCapacity = 0,
                 paddingBytes = 0):
        self.name = name
        self.url = url
        self.hasEncKey = hasEncKey
        self.encKey = bytes.fromhex(encKey)
        self.html = html
        self.status = status
        self.totalCapacity = totalCapacity
        self.realCapacity = realCapacity
        self.paddingBytes = paddingBytes

        if html is None:
            self.loadHTML()

    def computeCityCapacity(self):
        parsedHtml = BeautifulSoup(self.html, 'html.parser')
        temps = parsedHtml.find_all('span', attrs={'data-temp': True})

        self.totalCapacity = len(temps)
        self.realCapacity = self.totalCapacity - self.totalCapacity % BLOCK_SIZE
        self.paddingBytes = self.totalCapacity - self.realCapacity

    def loadHTML(self):
        response = requests.get(self.url)
        self.html = response.text
        self.status = response.status_code
        self.computeCityCapacity()

    def saveToFile(self):
        data = {
            'name': self.name,
            'url': self.url,
            'hasEncKey': self.hasEncKey,
            'encKey': self.encKey.hex(),
            'html': self.html,
            'status': self.status,
            'totalCapacity': self.totalCapacity,
            'realCapacity': self.realCapacity,
            'paddingBytes': self.paddingBytes
        }

        filename = CITIES_PATH + "{}.json".format(self.name)
        with open(filename, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def loadCityFromFile(cityName):
        try:
            filename = CITIES_PATH + cityName + ".json"
            with open(filename , 'r') as file:
                data = json.load(file)

            return CityData(data['name'],
                            data['url'],
                            data['hasEncKey'],
                            data['encKey'],
                            data['html'],
                            data['status'],
                            data['totalCapacity'],
                            data['realCapacity'],
                            data['paddingBytes'])
        except:
            return None