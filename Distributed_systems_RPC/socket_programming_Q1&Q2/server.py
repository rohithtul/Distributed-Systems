import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        messages = conn.recv(SIZE).decode(FORMAT)
        messages = messages.split("@")
        console_input = messages[0]
        console_input=console_input.lower()
        if console_input == "download":
            files = os.listdir(SERVER_DATA_PATH)
            sending_data_files = "OK@"

            if len(files) == 0:
                sending_data_files += "The server directory is empty"
            else:
                sending_data_files += "\n".join(f for f in files)
            conn.send(sending_data_files.encode(FORMAT))

        elif console_input == "upload":
            name, text = messages[1], messages[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

            sending_data_files = "OK@File uploaded successfully."
            conn.send(sending_data_files.encode(FORMAT))

        elif console_input == "delete":
            files = os.listdir(SERVER_DATA_PATH)
            sending_data_files = "OK@"
            filename = 'data.txt'

            if len(files) == 0:
                sending_data_files += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    sending_data_files += "File deleted successfully."
                else:
                    sending_data_files += "File not found."

            conn.send(sending_data_files.encode(FORMAT))
       
        elif console_input == "rename":
            files = os.listdir(SERVER_DATA_PATH)
            sending_data_files = "OK@"
            file_change = 'server_data/data.txt'
            new_name = 'server_data/new_data.txt'

            if len(files) == 0:
                sending_data_files += "The server directory is empty"
            else:
                if 'data.txt' in files:
                    os.rename(file_change,new_name )
                    sending_data_files += "File renamed successfully."
                else:
                    sending_data_files += "File not found."

            conn.send(sending_data_files.encode(FORMAT))
          
        elif console_input == "logout":
            break


    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)
     
if __name__ == "__main__":
    main()
