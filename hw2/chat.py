#!/usr/local/bin/python3
# Homework 2-Q4
# Sam Eakin

''' EXECUTE THESE FOR TESTING:

#### 1 to 1 connection ####
py chat.py user1 5001 127.0.0.1:5002
py chat.py user2 5002 127.0.0.1:5001

#### multiple connection ####

py chat.py user1 5001 127.0.0.1:5002 127.0.0.1:5003
py chat.py user2 5002 127.0.0.1:5001 127.0.0.1:5003
py chat.py user3 5003 127.0.0.1:5001

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
		self.serverSocket = None # socket client will listen on.
		self.writeSockets = [] # sockets for each client connection
		self.readSockets = [] # incoming connections from clients

	def getInputArgs(self): # 1[chat.py] 2[name] 3[port] 4[connection:port] 5[connection:port]
		arg_count = len(sys.argv)

		if arg_count < 3:
			print("Not enough arguments!")
			sys.exit(-1)
		elif arg_count == 3:
			print("Please enter connections!")
		else:
			self.name = sys.argv[1]
			self.port = int(sys.argv[2])
			self.IP = sys.argv[3].split(':')[0]
			arguments = sys.argv[3:]
			for arg in arguments:
				arg = arg.split(':')
				self.connections.append(int(arg[1]))

	def createListenSocket(self):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind((self.IP, self.port))
		self.serverSocket.listen()
		print('Listening on ', self.IP ,self.port)

	def eventLoop(self):
		while True:
			rlist = [self.serverSocket, sys.stdin]
			rlist.extend(self.readSockets)
			rlist_out, _, _ = select.select(rlist, [], [])

			for s in rlist_out:
				if s == self.serverSocket: # there is an incoming connection from a client
					conn, addr = s.accept()
					#print('Accepting incoming connection from', s.fileno())
					self.readSockets.append(conn)
				elif s == sys.stdin: # there is keyboard input to send
					txt = input()
					if len(self.writeSockets) == 0:
						self.connectToClients()
					self.sendMessage(txt)
				else: # this must be a socket to read from
					data = conn.recv(1024)
					if not data:
						print('Client Disconnected.')
						s.close()
						self.readSockets.remove(s) # remove read sockets
					else:
						#print('Received ', data.decode())
						self.unpackJSON(data.decode())

	def connectToClients(self): # from class
		for client in self.connections:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.IP, client))
			self.writeSockets.append(s)
			#print('Connected to client ', client)

	def sendMessage(self, message):
		if message == 'exit':
			self.closeConnection()
			sys.exit(-1)
		message = self.createJSON(message)
		message = message.encode()
		for s in self.writeSockets:
			#print('Sending to ', s.fileno())
			s.sendall(message)

	def createJSON(self, message): # {"seq": 0, "user": "user1", "message": "hello"}
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
		for s in self.writeSockets:
			s.close()
		for s in self.readSockets:
			s.close()
		self.serverSocket.close()
		print('All connections terminated. Goodbye.')
	
	def __str__(self):
		print('Client Initialized:')
		return '%s %s %s %s' % (self.name, self.port, self.IP, self.connections)

if __name__ == "__main__":
	user = Client(sys.argv[1])
	user.getInputArgs()

	user.createListenSocket()
	user.eventLoop()
#
#
#
#
#