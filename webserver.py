import http.server
import socketserver
import requests
from bs4 import BeautifulSoup

# Define the host and port for your server
HOST = "localhost"
PORT = 8000

MONTH = 'May'

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Make a GET request to the external website
        response = requests.get("https://www.tiempo3.com/europe/spain?page=month&month={}".format(MONTH))
        
        # Set response headers
        self.send_response(response.status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Send the response content
        self.wfile.write(response.content)

# Create an instance of the HTTP server with your request handler
with socketserver.TCPServer((HOST, PORT), MyHttpRequestHandler) as httpd:
    print("Server started at http://{}:{}".format(HOST, PORT))
    
    # Serve forever
    httpd.serve_forever()
