import socket
import os 
import shutil
IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
path_download='/home/rituraj/Music/socket_programming_Q1&Q2/download_data/new_data.txt'
source_data='/home/rituraj/Music/socket_programming_Q1&Q2/server_data/new_data.txt'
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        messages = client.recv(SIZE).decode(FORMAT)
        console_input, msg = messages.split("@")
        if console_input == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif console_input == "OK":
            print(f"{msg}")
	
        messages = input("> ")
        messages = messages.split(" ")
        console_input = messages[0]
        console_input=console_input.lower()
        #print(console_input)
 	     
        if console_input == "logout":
            client.send(console_input.encode(FORMAT))
            break
        elif console_input == "download":
          shutil.copy(source_data, path_download)
          client.send(console_input.encode(FORMAT))
		
        elif console_input == "rename" :
            client.send(f"{console_input}@{messages[0]}".encode(FORMAT))
        elif console_input == "delete":
            client.send(f"{console_input}@{messages[0]}".encode(FORMAT))
        elif console_input == "upload":
            path = '/home/rituraj/Music/socket_programming_Q1&Q2/client_data/data.txt'
            with open(f"{path}", "r") as f:
                text = f.read()
            filename = path.split("/")[-1]
            sending_data = f"{console_input}@{filename}@{text}"
            client.send(sending_data.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()
