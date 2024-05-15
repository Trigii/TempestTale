import listener
import messageManager
import webserver
import subprocess

def main():
    print("TempestTale tests")

    print("###########################################################################################################")
    print("Test 1: the listener attempts to extract a message with the server not running")
    inputs = ['Teruel']
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()

    # Split the output into lines
    output_lines = output.splitlines()

    # Print each line of the output separately
    i = 0
    for line in output_lines:
        print(line + inputs[i] + '\n')
        i = i+1

    print("Spawning the C2 server")
    server = subprocess.Popen(['python3', 'webserver.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    print("###########################################################################################################")
    print("Test 2: the listener attempts to extract a message that dont exist")
    inputs = ['Vigo', 'password']
    p1 = subprocess.Popen(['python3', 'listener.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for inp in inputs:
        p1.stdin.write(inp + '\n')
        p1.stdin.flush()

    # Read the output of the subprocess
    output, _ = p1.communicate()
    print(output)
    # Split the output into lines
    output_lines = output.splitlines()


    






    print("Killing the server...")
    server.terminate()


if __name__ == "__main__":
    main()