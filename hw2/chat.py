#!/usr/local/bin/python3
# Homework 2-Q4
# Sam Eakin

''' EXECUTE THESE FOR TESTING:

py chat.py user1 5001 127.0.0.1:5002
py chat.py user2 5002 127.0.0.1:5001

py chat.py user1 5001 127.0.0.1:5002 127.0.0.1:5003

'''

import sys
import socket
import select

HOST = '127.0.0.1' # The server's hostname or IP address

class Client:
	def __init__(self, name):
		self.name = name
		self.port = None
		self.IP = None
		self.connections = []
		self.sel = None
		self.lsock = None # socket client will listen on.
		self.wsock = None # socket client will send on.
		self.message = ''

	# 1[chat.py] 2[name] 3[port] 4[connection:port] 5[connection:port]
	def getInput(self):
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
		print('Setting up listening socket:')
		self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.lsock.bind((self.IP, self.port))
		self.lsock.listen()
		print('Listening on ',(self.IP, self.port))

	def createMessage(self):
		print('Welcome to the Chat: ')
		message = input()
		message = message.encode()
		self.message = message

	def sendMessage(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((self.IP, self.connections[0]))
			s.sendall(self.message)
			#data = s.recv(1024)
			#print ('Recieved', repr(data))

	def getMessage(self):
		self.wsock, addr = self.lsock.accept() 
		# The with statement is used with conn to automatically close the socket at the end of the block.
		print('Connected by', addr)
		while True:
			data = self.wsock.recv(1024)
			if not data:
				break
			print(data)
			self.wsock.sendall(data)
	
	def __str__(self):
		print('Client Initialized:')
		return '%s %s %s %s' % (self.name, self.port, self.IP, self.connections)

if __name__ == "__main__":
	user = Client(sys.argv[1])
	user.getInput()
	print(user)

	user.createListenSocket()

	# ---- This is where I'm stuck ---- #
	# How do I create an event loop that will print any messages recieved
	# over the listening socket? It also has to be waiting for any typed input to send.

	user.createMessage()

	user.sendMessage()



#
#
#
#
#
#
