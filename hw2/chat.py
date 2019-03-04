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
import selectors

HOST = '127.0.0.1' # The server's hostname or IP address

class Client:
	def __init__(self, name):
		self.name = name
		self.port = None
		self.IP = None
		self.connections = []
		self.sel = None
		self.lsock = None
		self.message = ''

	# 1[chat.py] 2[name] 3[port] 4[connection:port] 5[connection:port]
	def getInput(self):
		arg_count = len(sys.argv)

		if arg_count < 3:
			print("Not enough arguments!")
		elif arg_count == 3:
			print("Please enter connections!")
		else:
			self.name = sys.argv[1]
			self.port = int(sys.argv[2])
			self.IP = sys.argv[3].split(':')[0]
			arguments = sys.argv[3:]
			for arg in arguments:
				arg = arg.split(':')
				self.connections.append(arg[1])

	def createListenSocket(self):
		print('Setting up listening socket:')
		self.sel = selectors.DefaultSelector()
		self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.lsock.bind((self.IP, self.port))
		self.lsock.listen()
		print('Listening on ',(self.IP, self.port))
		self.lsock.setblocking(False)
		self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

	def createMessage(self):
		print('Enter your message: ')
		message = input()
		message = message.encode()
		self.message = message

	def sendMessage(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((self.IP, int(self.connections[0])))
			s.sendall(self.message)

	def getMessage(self):
		conn, addr = lsock.accept() 
		# The with statement is used with conn to automatically close the socket at the end of the block.
		with conn:
			print('Connected by', addr)
			while True:
				data = conn.recv(1024)
				if not data:
					break
				print(data)
				conn.sendall(data)
	
	def __str__(self):
		print('Client Initialized:')
		return '%s %s %s %s' % (self.name, self.port, self.IP, self.connections)

class Packet:
	pass

if __name__ == "__main__":
	# parse command line arguments
	user = Client(sys.argv[1])
	user.getInput()
	print(user)

	user.createListenSocket()

	user.createMessage()
	print(user.message)

	user.sendMessage()



#
#
#
#
#
#