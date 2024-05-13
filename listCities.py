import http.server
import socketserver
import requests
from bs4 import BeautifulSoup

def extract_city_names_and_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    cities = []
    urls = []
    
    for option in soup.find_all('option'):
        city_name = option.text.strip()
        city_url = option['value']
        cities.append(city_name)
        urls.append(city_url)
    
    return cities, urls
    

month = 'May'

response = requests.get("https://www.tiempo3.com/europe/spain?page=month&month={}".format(month))

(cities, urls) = extract_city_names_and_urls(response.text)

for (i, city) in enumerate(cities):
    print("City: " + city)
    print("Url: " + urls[i])
    print()
