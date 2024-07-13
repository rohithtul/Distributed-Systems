import socket
import os
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 15555))
while True:
    print('write as operation to be performed=add/sort/pi/multiply, num1, num2')
    print('For multiplication and sort provide two or more separate lists')
    print('In multiplication list and operator is separated by *')
    inp = input("Enter the operation such as sort, add, multiply and pi: ")
    if inp == "Over":
      client.send(inp.encode())
      break
    client.send(inp.encode())
    answer = client.recv(1024)
    print("Answer is "+answer.decode())
    print("Type 'Over' to terminate")
 
client.close()
