# server.py
# Networking Homework 4
# Sam Eakin
# 4/8/19

'''
--start server--
python server.py 127.0.0.1:8000

--web input--
http://127.0.0.1:8000/car.html
'''

import sys
import types
import socket
import selectors

# [server.py][IP:port]
def getInputArgs():
	arg_count = len(sys.argv)
	if arg_count < 2:
		print("Not enough arguments!")
		sys.exit(-1)
	elif arg_count == 1:
		print("Please enter IP:PORT!")
	else:
		inputArg = sys.argv[1].split(':')
		IP = inputArg[0]
		port = int(inputArg[1])
		return IP, port

def accept_wrapper(sock):
	conn, addr = sock.accept()  # Should be ready to read
	print('accepted connection from', addr)
	conn.setblocking(False)
	data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	sel.register(conn, events, data=data)

def service_connection(key, mask):
	sock = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		recv_data = sock.recv(1024)  # Should be ready to read
		if recv_data:
			data.outb += recv_data
		else:
			print('closing connection to', data.addr)
			sel.unregister(sock)
			sock.close()
	if mask & selectors.EVENT_WRITE:
		if data.outb:
			filedata = process_http_header(sock, data.outb)
			#print('echoing', repr(data.outb), 'to', data.addr)
			#sent = sock.send(data.outb)  # Should be ready to write
			filedata = create_header(filedata)
			sent = sock.send(filedata.encode())
			data.outb = data.outb[sent:]

def process_http_header(socket, data):
	header = str(data.decode())
	#print(header)
	header_items = header.split('\r\n')
	request_item = header_items[0].split(' ')
	host_item = header_items[1].split(': ')
	host = host_item[1]

	print("****REQUEST****")
	print(request_item)
	print("****URI****")
	print(host)

	# testing a bad request
	bad_request = ['GET','/car.html','HTTP/1.0']

	valid_request = check_bad_request(request_item)
	file_exists = check_file_exist(request_item)
	return file_exists

def create_header(data):
	header = 'HTTP/1.1 200 OK \r\nContent-Type:text/html\r\n\r\n'
	return header+data

def check_file_exist(request):
	URL = 'static/' + request[1]
	with open(URL) as file:
		filedata = file.read()
		return filedata


def check_bad_request(request):
	if request[0] != 'GET':
		print('Error: Invalid GET')
		return False
	if type(request[1]) != str:
		print('Error: Invalid URI')
		return False
	if request[2] != 'HTTP/1.1':
		print('Error: Invalid HTTP version')
		return False
	else:
		print('Valid Request!')
		return True


##########################

sel = selectors.DefaultSelector()
# ...
host, port = getInputArgs()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

while True:
	events = sel.select(timeout=None)
	for key, mask in events:
		if key.data is None:
			accept_wrapper(key.fileobj)
		else:
			service_connection(key, mask)



