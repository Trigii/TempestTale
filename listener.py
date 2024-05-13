import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
import json
from Crypto.Cipher import AES

# Define the host and port for your server
HOST = "localhost"
PORT = 8000

MONTH = 'May'

def parseData(html):
    parsedHtml = BeautifulSoup(html, 'html.parser')

    # Find all <span> elements with data-temp attribute
    temps = parsedHtml.find_all('span', attrs={'data-temp': True})

    data = []

    # Modify the data-temp attribute of each <span> element
    for (i, temp) in enumerate(temps):

        span = temps[i]
        tempMd = int(float(span['data-temp']) * 10)
        temp = int(float(span.text) * 10)

        byte = tempMd - temp
        data.append(byte)

    return data


city = input("Enter city name: ")

response = requests.get("http://{}:{}/?city={}".format(HOST, PORT, city))

data = parseData(response.text)

# Remove padding
last_byte = data[-1]
if data[-last_byte] == last_byte:
    data = data[:-last_byte]

data = bytes(data)

# Generate key
userKey = input("Enter encryption key: ")

key_padded = userKey.encode('utf-8').ljust(16, b'\0')

cipher = AES.new(key_padded, AES.MODE_ECB)


# Decrypt the message
msgDec = cipher.decrypt(data)

print(msgDec.split(b'\0')[0].decode('utf-8'))