#!/usr/local/bin/python3
# Homework 2-Q5
# chat5.py
# Sam Eakin

''' EXECUTE THESE FOR TESTING:

py chat5.py user1 5002 127.0.0.1:5001
py chat5.py user2 5003 127.0.0.1:5001
py chat5.py user3 5004 127.0.0.1:5001

'''

import json
import sys
import socket
import select

HOST = '127.0.0.1' # LOCALHOST is used for all connections

class Client:
	def __init__(self, name):
		# System Args
		self.name = name
		self.port = None
		self.IP = None
		self.connections = [] # port numbers to connect to
		# Communication Args
		self.seq = 0 # message sequence number 
		self.sel = None
		self.listenSocket = None # socket client will listen on.
		self.serverSocket = [] # sockets for each client connection
		self.readSockets = [] # incoming connections from clients

	# 1[chat.py] 2[name] 3[port] 4[connection:port]
	def getInputArgs(self):
		arg_count = len(sys.argv)

		if arg_count < 3:
			print("Not enough arguments!")
			sys.exit(-1)
		elif arg_count == 3:
			print("Please enter server connection!")
		else:
			self.name = sys.argv[1]
			self.port = int(sys.argv[2])
			self.IP = sys.argv[3].split(':')[0]
			serverArg = sys.argv[3].split(':')
			self.connections.append(int(serverArg[1]))

	def createListenSocket(self):
		print('Setting up listening socket:')
		self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listenSocket.bind((self.IP, self.port))
		self.listenSocket.listen()
		print('Listening on ', self.listenSocket)

	def eventLoop(self):
		# send the subscribe command
		while True:
			rlist = [sys.stdin]
			rlist.extend(self.readSockets)
			rlist_out, _, _ = select.select(rlist, [], [])

			for s in rlist_out:				
				if s == sys.stdin: # there is keyboard input to send
					txt = input()
					if len(self.serverSocket) == 0:
						self.connectToServer()
					self.sendMessage(txt)
				else: # this must be a socket to read from
					data = conn.recv(1024)
					if not data:
						print('Stopped')
						s.close()
						self.readSockets.remove(s) # remove read sockets
					else:
						print('Received ', data.decode())
						self.unpackJSON(data.decode())

	# from class
	def connectToServer(self):
		for client in self.connections:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print('Connecting to client ', client)
			s.connect((self.IP, client))
			self.serverSocket.append(s)
			print('Connected to client ', client)
			print(s)

	def sendMessage(self, message):
		if message == 'exit':
			self.closeConnection()
			sys.exit(-1)
		message = self.createJSON(message)
		message = message.encode()
		for s in self.serverSocket:
			print('Sending to ', s.fileno())
			s.sendall(message)

	# {"seq": 0, "user": "user1", "message": "hello"}
	def createJSON(self, message):
		message = json.dumps({'seq': self.seq, 'user': self.name, 'message': message})
		self.seq += 1
		return message

	def unpackJSON(self, JSONmessage):
		message = json.loads(JSONmessage)
		data = []
		for key,value in message.items():
			data.append(value)
		print('%s: %s' % (data[1], data[2]))


	def closeConnection(self):
		for s in self.serverSocket:
			s.close()
		for s in self.readSockets:
			s.close()
		self.listenSocket.close()
		print('All connections terminated. Goodbye.')
	
	def __str__(self):
		print('Client Initialized:')
		return '%s %s %s %s' % (self.name, self.port, self.IP, self.connections)


if __name__ == "__main__":
	user = Client(sys.argv[1])
	user.getInputArgs()
	print(user)

	user.eventLoop()
#
#
#
#
#