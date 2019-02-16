#!/usr/local/bin/python3

import socket

# In comparison to the server, the client is pretty simple. 
# It creates a socket object, connects to the server and calls s.sendall() to send its message. 
# Lastly, it calls s.recv() to read the server’s reply and then prints it.

HOST = '127.0.0.1' # The server's hostname or IP address
PORT = 65432 # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	s.sendall(b'Hello World!')
	data = s.recv(1024)

print('Received', repr(data))