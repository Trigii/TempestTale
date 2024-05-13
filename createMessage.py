import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
import json

from Crypto.Cipher import AES

MONTHS= ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class City():
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.totalCapacity = 0
        self.realCapacity = 0
        self.paddingBytes = 0

    def computeCapacity(self):
        response = requests.get(self.url)
        html = response.text
        parsedHtml = BeautifulSoup(html, 'html.parser')

        temps = parsedHtml.find_all('span', attrs={'data-temp': True})

        self.totalCapacity = len(temps)
        self.realCapacity = self.totalCapacity - self.totalCapacity % AES.block_size
        self.paddingBytes = self.totalCapacity - self.realCapacity


def getCities(month):
    response = requests.get("https://www.tiempo3.com/europe/spain?page=month&month={}".format(month))
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    cityList = []
    for option in soup.find_all('option'):
        city_name = option.text.strip()
        city_url = option['value']
        cityList.append(City(city_name, city_url))

    return cityList

def selectCity(cities):
    for (i, city) in enumerate(cities):
        print("{}. City: {}".format(i + 1, city.name))
        print()

    while True:
        cityNum = int(input("Enter city number: "))
        if cityNum > 0 and cityNum <= len(cities):
            break
        print("Invalid city number")

    return cities[cityNum - 1]

print("Welcome to the weather forecast program!")

month = 0

while True:
    monthNum = int(input("Enter current month number (1-12): "))
    if monthNum > 0 and monthNum < 13:
        month = MONTHS[int(monthNum) - 1]
        break
    print("Invalid month number")

# Get list of cities
cityList = getCities(month)

# Select city
city = selectCity(cityList)

# Compute Capacity
city.computeCapacity()
print("City {} has a capacity of {} bytes".format(city.name, city.realCapacity))

# Get message
while True:
    msg = input("Enter message: ")
    if len(msg) <= city.realCapacity:
        break
    print("Message too long. Maximum length is {} bytes".format(city.realCapacity))

# Padding the message
msg_padded = msg.encode('utf-8')
msg_padded += b'\0' * (city.realCapacity - len(msg_padded))

# Encrypt message
userKey = input("Enter encryption key: ")
key_padded = userKey.encode('utf-8').ljust(16, b'\0')
cipher = AES.new(key_padded, AES.MODE_ECB)
msg_enc = cipher.encrypt(msg_padded)

# Add padding
encData = msg_enc + bytes([city.paddingBytes]) * city.paddingBytes

# Format data to integer list
data = list(encData)

cityInfo = {
    "name": city.name,
    "url": city.url,
    "msg": data
}

filename = "./cities/{}.json".format(city.name)

with open(filename, "w") as file:
    json.dump(cityInfo, file)

print("Weather data saved to {}".format(filename))