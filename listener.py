import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
import json
from Crypto.Cipher import AES
from decimal import Decimal as D

# Define the host and port for your server
HOST = "localhost"
PORT = 8000

def toFarht(celsius):
    return D((celsius * D(9)/D(5)) + D(32))

# Parse the data from the HTML
def parseData(html):
    parsedHtml = BeautifulSoup(html, 'html.parser')

    # Find all <span> elements with data-temp attribute
    temps = parsedHtml.find_all('span', attrs={'data-temp': True})

    data = []

    # Modify the data-temp attribute of each <span> element
    for (i, temp) in enumerate(temps):

        span = temps[i]
        tempCelsius = D(span['data-temp'])

        farhtMd = D(span['data-temp-farht'])

        byte = (farhtMd - toFarht(tempCelsius)) * D(100)
        data.append(int(byte))

    return data

# Get the encryption key
def getEncKey(response):

    # Get the encryption key from the response cookies
    sessionId = response.cookies.get('sessionId')
    if sessionId is not None:
        return bytes.fromhex(sessionId)

    userKey = input("Enter encryption key: ")

    try:
        userKey = bytes.fromhex(userKey)
    except:
        userKey = userKey.encode('utf-8')

    return userKey.ljust(16, b'\0')

# Decrypt the data
def decryptData(data, encKey):
    # Remove padding
    last_byte = data[-1]
    if data[-last_byte] == last_byte:
        data = data[:-last_byte]

    data = bytes(data)

    # Decrypt the message
    cipher = AES.new(encKey, AES.MODE_ECB)
    msgDec = cipher.decrypt(data)

    return msgDec

# Main function
def main():
    city = input("Enter city name: ")

    response = requests.get("http://{}:{}/?city={}".format(HOST, PORT, city))

    if response.status_code != 200:
        print("Invalid city")
        return

    encKey = getEncKey(response)

    encData = parseData(response.text)

    data = decryptData(encData, encKey)

    print(data.split(b'\0')[0].decode('utf-8'))

if __name__ == "__main__":
    main()