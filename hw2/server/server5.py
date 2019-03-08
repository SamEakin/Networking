#!/usr/local/bin/python3
# Homework 2-Q5
# server5.py
# Sam Eakin
''' 
EXECUTE THIS TO RUN SERVER:

py server5.py 127.0.0.1:5001

'''
import json
import sys
import socket
import select

class Server:
	def __init__(self, name):
		# System Args
		self.IP = None
		self.port = None
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
		elif arg_count == 1:
			print("Please enter IP:PORT!")
		else:
			inputArg = sys.argv[1].split(':')
			self.IP = inputArg[0]
			self.port = int(inputArg[1])

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
						print('Client closed the connection:', addr)
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