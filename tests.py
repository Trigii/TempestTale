import listener
import messageManager
import webserver
import subprocess
import re
import time

def extract_key(hex_string):
    pattern = r'\bkey: ([0-9a-fA-F]{32})\b'
    matches = re.findall(pattern, hex_string)
    return matches[0] if matches else None

PASS = 'TEST PASSED'
FAIL = 'TEST FAILED'
SERVER_FAIL = 'SERVER FAILED'

def startServer():
    return subprocess.Popen(['python3', 'webserver.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def stopServer(server):
    print("Killing the server...")
    server.terminate()

def main():

    print("TempestTale tests")

    ######## 
    # Test 1
    ########

    print("\n" + "#" * 50)
    print("Test 1: the listener attempts to extract a message with the server not running")
    inputs = ['A Coruña']
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()
    if 'Server not found' in output: print(PASS)
    else: print(FAIL)

    ##############
    # Start server
    ##############

    server = startServer()
    time.sleep(3)

    ######## 
    # Test 2
    ########

    print("\n" + "#" * 50)
    print("Test 2: the listener attempts to extract a message that dont exist")
    inputs = ['London', 'password']
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()
    if 'Invalid city' in output: print(PASS)
    elif 'Server not found' in output: print(SERVER_FAIL)
    else: print(FAIL)

    # Split the output into lines
    output_lines = output.splitlines()

    ######## 
    # Test 3: extract with user generated password with manual input
    ########

    print("\n" + "#" * 50)
    print("Test 3: extract with user generated password with manual input")

    inputs = ['y', '1', 'Test message', 'm', 'password', 'n', 'n']
    p1 = subprocess.Popen(['python3', 'messageManager.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()
    output, _ = p1.communicate()
    time.sleep(3)

    inputs = ['A Coruña', 'password']
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()
    if 'Test message' in output: print(PASS)
    elif 'Server not found' in output: print(SERVER_FAIL)
    else: print(FAIL)

    ######## 
    # Test 4: extract with user generated password with cookie
    ########

    print("\n" + "#" * 50)
    print("Test 4: extract with user generated password with cookie")

    inputs = ['y', '1','Test message', 'm', 'password', 'y', 'n']
    p1 = subprocess.Popen(['python3', 'messageManager.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()
    output, _ = p1.communicate()
    time.sleep(3)

    inputs = ['Adeje']
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()
    
    if 'Test message' in output: print(PASS)
    elif 'Server not found' in output: print(SERVER_FAIL)
    else: print(FAIL)

    ######## 
    # Test 5: extract with random password with cookie
    ########

    print("\n" + "#" * 50)
    print("Test 5: extract with random password with cookie")

    inputs = ['y', '1','Test message', 'r', 'y', 'n']
    p1 = subprocess.Popen(['python3', 'messageManager.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()
    output, _ = p1.communicate()

    time.sleep(3)

    inputs = ['Aguilas']
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()
    
    if 'Test message' in output: print(PASS)
    elif 'Server not found' in output: print(SERVER_FAIL)
    else: print(FAIL)

    ######## 
    # Test 6: extract with random password with manual input
    ########

    print("\n" + "#" * 50)
    print("Test 6: extract with random password with manual input")

    inputs = ['y', '1','Test message', 'r', 'n', 'n']
    p1 = subprocess.Popen(['python3', 'messageManager.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()
    output, _ = p1.communicate()
    key = extract_key(output)
    time.sleep(3)

    inputs = ['Ainsa', key]
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()
    
    if 'Test message' in output: print(PASS)
    elif 'Server not found' in output: print(SERVER_FAIL)
    else: print(FAIL)


    #############
    # Stop server
    #############

    stopServer(server)


if __name__ == "__main__":
    main()