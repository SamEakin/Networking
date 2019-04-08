# server.py
# Networking Homework 4
# Sam Eakin
# 4/8/19

import sys
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
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

##########################
#host = '127.0.0.1'
#port = 8000

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