#!/usr/local/bin/python3

# Socket Programming Tutorial
# https://realpython.com/python-sockets/#socket-api-overview
# TO RUN: 
# 1. make the python file an executable chmod +x filename.py
# 2. ./filename.py

import socket

HOST = '127.0.0.1' # LocalHost 
PORT = 65432 # Port to listen on (non-reserved ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # AF_INET = IPv4 / SOCK_STREAM = TCP socket type
	s.bind((HOST, PORT))
	s.listen()

	# One thing that’s imperative to understand is that we now have a new socket object from accept().
	# accept() blocks and waits for an incoming connection. When a client connects, it returns a new socket object representing the connection and a tuple holding the address of the client.
	# The tuple will contain (host, port) for IPv4 connections or (host, port, flowinfo, scopeid) for IPv6. See Socket Address Families in the reference section for details on the tuple values.
	conn, addr = s.accept() 

	# The with statement is used with conn to automatically close the socket at the end of the block.
	with conn:
		print('Connected by', addr)
		while True:
			data = conn.recv(1024)
			if not data:
				break
			conn.sendall(data)