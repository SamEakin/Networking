#!/usr/local/bin/python3
# Homework 2-Q4
# Sam Eakin

''' EXECUTE THIS:
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
		# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
	def __str__(self):
		return '%s %s %s %s' % (self.name, self.port, self.IP, self.connections)

if __name__ == "__main__":
	# parse command line arguments
	user = Client(sys.argv[1])
	user.getInput()
	print(user)

	# create listening socket and start listening
	lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	lsock.bind((user.IP, user.port))
	lsock.listen()
	print('Listening on ',(user.IP, user.port))
	#conn, addr = lsock.accept()
	lsock.close()
	'''
	print('Connected by', addr)
	while True:
		data = conn.recv(1024)
		if not data:
			break
		conn.sendall(data)

	'''
