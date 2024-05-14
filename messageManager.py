import json
import secrets

from Crypto.Cipher import AES

from bs4 import BeautifulSoup
from decimal import Decimal as D

from DB import City, TempestDB
from CityData import CityData, BLOCK_SIZE

DB = TempestDB.loadFromFile()

def selectCity():

    # Filter cities that are not in use
    availableCities = [city for city in DB.cities.values() if not city.onUse]

    # Print available cities
    for (i, city) in enumerate(availableCities):
        print("{:3}. {}".format(i + 1, city.name))

    while True:
        cityName = input("Enter city number: ")
        if cityName.isdigit():
            cityNum = int(cityName)
            if cityNum > 0 and cityNum <= len(availableCities):
                break
            print("Invalid city number")

    return availableCities[cityNum - 1]

# Message generation
def getMessage(maxLength):
    while True:
        msg = input("Enter message (limit: {}B): ".format(maxLength))
        if len(msg) <= maxLength:
            return msg
        print("Message too long. Maximum length is {} bytes".format(maxLength))

def is_hexadecimal(s):
    try:
        bytes.fromhex(s)
        return True
    except ValueError:
        return False

# Key management
def generateKey():
    userInput = input("Do you want to use a randomly generated key or to use a custom key?[R/m] ").lower()
    while userInput != 'r' and userInput != 'm' and userInput != '':
        userInput = input("Invalid input. Do you want to use a randomly generated key or a custom password?[R/m] ").lower()

    if userInput == 'm':
        userKey = ""
        while len(userKey) == 0:
            userIn = input("Enter encryption key: ")

            if is_hexadecimal(userIn) and len(userIn) == 32: 
                userKey = userIn
                break
            elif len(userIn) <= 16 and len(userIn) != 0:
                userKey = userKey.encode('utf-8')
                break

            print("Invalid key!")

        return userKey.ljust(16, b'\0')

    encKey =  secrets.token_bytes(16)
    print("Encryption key: {}".format(encKey.hex()))

    return encKey

def keyTransmission():
    userInput = input("Do you want to send the key hidden as a session id cookie?[Y/n]").lower()
    while userInput != 'y' and userInput != 'n' and userInput != '':
        userInput = input("Invalid input. Do you want to send the key hidden as a session id cookie?[Y/n] ").lower()

    return userInput != 'n'

# Encryption
def encryptMessage(msg, encKey, city):
    # Padding the plaintext
    msg = msg.encode('utf-8')
    msg += b'\0' * (city.realCapacity - len(msg))

    # Encrypt message
    AES.block_size = BLOCK_SIZE
    cipher = AES.new(encKey, AES.MODE_ECB)
    msgCiph = cipher.encrypt(msg)

    # Add outer padding
    encData = msgCiph + bytes([city.paddingBytes]) * city.paddingBytes

    return list(encData)


# Steganography functions

def toFarht(celsius):
    return (celsius * D(9)/D(5)) + D(32)

def modifyTemps(html, data):
    parsedHtml = BeautifulSoup(html, 'html.parser')

    # Find all <span> elements with data-temp attribute
    temps = parsedHtml.find_all('span', attrs={'data-temp': True})

    # Modify the data-temp attribute of each <span> element
    for (i, byte) in enumerate(data):

        if len(temps) <= i:
            break

        span = temps[i]
        temp = D(span['data-temp'])
        fahrenheit = toFarht(temp)

        # Hide byte
        modifiedFahrenheit = fahrenheit + D(data[i]) / 100

        span['data-temp-farht'] = str(modifiedFahrenheit)

    # Return the modified HTML
    return str(parsedHtml)

# Message creation

def createMessage():
    # User selects city
    city = selectCity()

    cityData = CityData(city.name, city.url)

    # Get message capacity
    msg = getMessage(cityData.realCapacity)

    # Generate encryption key
    encKey = generateKey()

    # Key transmission
    keyTrans = keyTransmission()

    # Encrypt message
    encData = encryptMessage(msg, encKey, cityData)

    # Save data in city html
    cityData.html = modifyTemps(cityData.html, encData)

    # Save key in city data
    if keyTrans:
        cityData.hasEncKey = True
        cityData.encKey = encKey

    # Save message in city data
    cityData.saveToFile()

    # Update DB
    DB.useCity(cityData.name)
    DB.saveInFile()

# Main function
def main():

    print("Welcome to TempesTale!")

    if DB is None:
        print("Error loading database")
        return

    while True:
        print("\n" * 3)
        DB.displayStatus()
        print("\n" * 2)

        if input("Do you want to send a message?[y/n] ").lower() == 'n':
            break

        createMessage()


if __name__ == "__main__":
    main()