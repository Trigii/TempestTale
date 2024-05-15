import http.server
import socketserver

from urllib.parse import urlparse, parse_qs
import datetime

from DB import City, TempestDB
from CityData import CityData

# Define the host and port for your server
HOST = "localhost"
PORT = 8000

DB = None

# HTTP server

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global DB
        # Parse the query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Extract the value of the "city" parameter
        cityName = query_params.get('city', [None])[0]

        if cityName is None or not DB.hasCity(cityName):
            self.send_response(400)
            self.end_headers()
            return

        # Load the city from the database
        city = CityData.loadCityFromFile(cityName)
        if city is None or city.html is None:
            self.send_response(400)
            self.end_headers()
            return

        # Set response headers
        self.send_response(city.status)
        self.send_header("Content-type", "text/html")

        # Set the encryption key in the response cookies
        if city.hasEncKey:
            self.send_header("Set-Cookie", "sessionId={}; Path=/".format(city.encKey.hex())) 

        self.end_headers()
        
        # Send the HTML content
        self.wfile.write(city.html.encode())


def initDB():
    global DB

    # Load the database
    DB = TempestDB.loadFromFile()

    # Check if the database is still valid
    if DB is None or DB.notValidAfter < datetime.datetime.now():
        DB = TempestDB()

        # Load cities
        DB.loadCities()

        # Save the database
        DB.saveInFile()

def startServer():
    # Create an instance of the HTTP server with your request handler
    with socketserver.TCPServer((HOST, PORT), MyHttpRequestHandler) as httpd:
        print("Server started at http://{}:{}".format(HOST, PORT))

        # Serve forever
        httpd.serve_forever()

def main():

    # Initialize the database
    initDB()

    # Start the server
    startServer()


if __name__ == "__main__":
    main()