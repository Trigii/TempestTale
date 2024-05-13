import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, parse_qs

# Define the host and port for your server
HOST = "localhost"
PORT = 8000

MONTH = 'May'

class City():
    def __init__(self, name, url, msg):
        self.name = name
        self.url = url
        self.msg = msg
    
    def loadCityFromFile(fileName):
        with open("cities/{}.json".format(fileName), 'r') as file:
            json_data = json.load(file)

        return City(json_data['name'], json_data['url'], json_data['msg'])

def modifyTemps(html, data):
    parsedHtml = BeautifulSoup(html, 'html.parser')

    # Find all <span> elements with data-temp attribute
    temps = parsedHtml.find_all('span', attrs={'data-temp': True})

    # Modify the data-temp attribute of each <span> element
    for (i, byte) in enumerate(data):

        if len(temps) <= i:
            break

        span = temps[i]
        temp = span['data-temp']

        modified_temp = int(temp) + int(data[i]) / 10

        span['data-temp'] = str(modified_temp)

    # Return the modified HTML
    return str(parsedHtml)

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        # Parse the query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Extract the value of the "city" parameter
        cityName = query_params.get('city', [None])[0]

        if cityName is None:
            self.send_response(400)
            self.end_headers()
            return

        city = City.loadCityFromFile(cityName)

        print(city.url)

        # Make a GET request to the forecast website
        response = requests.get(city.url)
        
        # Modify the HTML content
        html = response.text
        modified_html = modifyTemps(html, city.msg)

        # Set response headers
        self.send_response(response.status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Send the modified HTML content
        self.wfile.write(modified_html.encode())

# Create an instance of the HTTP server with your request handler
with socketserver.TCPServer((HOST, PORT), MyHttpRequestHandler) as httpd:
    print("Server started at http://{}:{}".format(HOST, PORT))

    # Serve forever
    httpd.serve_forever()