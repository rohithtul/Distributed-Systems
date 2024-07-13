import math
import numpy as np
import socket
import threading
import json
import ast
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 15555))
server.listen(8)
msg = ''

def handler(conn):
  def add(num1,num2):
    return num1+num2

  def calculate_pi():
    return math.pi

  def sort(arrayA):
    return sorted(arrayA)

  def matrix_multiply(matrixA, matrixB, matrixC):
    new_matrix=[[sum(i*j for i,j in zip(r,c)) for c in zip(*matrixB)] for r in matrixA]
    result=[[sum(i*j for i,j in zip(r,c)) for c in zip(*matrixC)] for r in new_matrix]
    return result

  def unicode(string_unicode):
    return ast.literal_eval(string_unicode)

  while True:
      data = conn.recv(1024)
      msg = data.decode()
      data=msg.split()
      if data[0] == 'Over':
          print("Connection is Over")
          break
      elif data[0] == "add":
        msg=msg.split()
        num1=int(msg[1])
        num2=int(msg[2])
        result =add(num1,num2)
      elif data[0] == "pi":
          result = calculate_pi()
      elif data[0] == "sort":
          msg=msg.split()
          arrayA=unicode(msg[1])
          result = sort(arrayA)
      elif data[0] == "multiply":
          msg=msg.split('*')
          matrixA, matrixB, matrixC=unicode(msg[1]), unicode(msg[2]), unicode(msg[3])
          result = matrix_multiply(matrixA, matrixB, matrixC)
  
      print("Send the result to client")
      output = str(result)
      conn.send(output.encode())
  conn.close()


while True:
    conn, addr =server.accept()
    t = threading.Thread(target=handler, args=(conn,))
    t.start()















