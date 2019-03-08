#!/usr/local/bin/python3
# Homework 2-Q5
# server5.py
# Sam Eakin
''' 
EXECUTE THIS TO RUN SERVER:

py server5.py server 5001

'''
import json
import sys
import socket
import select

HOST = '127.0.0.1' # LOCALHOST is used for all connections

class Server:
	def __init__(self, name):
		# System Args
		self.name = name
		self.port = None
		self.IP = None
		self.connections = [] # port numbers to connect to
		# Communication Args
		self.seq = 0 # message sequence number 
		self.sel = None
		self.serverSocket = None # socket client will listen on.
		self.writeSockets = [] # sockets for each client connection
		self.clientSockets = [] # incoming connections from clients

	# [server5.py][name][port]
	def getInputArgs(self):
		arg_count = len(sys.argv)

		if arg_count < 2:
			print("Not enough arguments!")
			sys.exit(-1)
		elif arg_count == 2:
			print("Please enter port!")
		else:
			self.name = sys.argv[1]
			self.port = int(sys.argv[2])
			self.IP = HOST

	def createListenSocket(self):
		print('Setting up Server Socket:')
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind((self.IP, self.port))
		self.serverSocket.listen()
		print('Server online: ',(self.IP, self.port))

		# from class
	def connectToClients(self):
		for client in self.connections:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print('Connecting to client ', client)
			s.connect((self.IP, client))
			self.writeSockets.append(s)
			print('Connected to client ', client)

	def sendMessage(self, message):
		print(message)
		for s in self.writeSockets:
			print('Sending to ', s.fileno())
			s.sendall(message)

	def eventLoop(self):
		while True:
			rlist = [self.serverSocket]
			rlist.extend(self.clientSockets)
			rlist_out, _, _ = select.select(rlist, [], [])

			for s in rlist_out:
				if s == self.serverSocket: # there is an incoming connection from a client
					conn, addr = s.accept()
					self.clientSockets.append(conn)
					print('Accepted connection from', addr)

				else: # this must be a client's socket to read from
					data = conn.recv(1024)
					if not data:
						print('%s closed the connection.', s.fileno())
						s.close()
						self.clientSockets.remove(s) # remove read sockets
					else:
						print('Received ', data)
						self.sendMessage(data)
						print('Message sent to client:')
						print(s)

if __name__ == "__main__":
	server = Server(sys.argv[1])
	server.getInputArgs()

	server.createListenSocket()
	server.eventLoop()

#
#
#
#
#