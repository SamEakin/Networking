# client.py
# Networking Homework 4
# Sam Eakin
# 4/8/19
'''
python client.py user1 127.0.0.1:8001 127.0.0.1:8000
'''

import sys
import types
import socket
import selectors

# [client.py] [name] [IP:port] [server]
def getInputArgs():
	arg_count = len(sys.argv)
	if arg_count < 4:
		print("Not enough arguments!")
		print("[client.py] [name] [IP:port] [server]")
		sys.exit(-1)
	else:
		name = sys.argv[1]
		inputArg = sys.argv[2].split(':')
		client_IP = inputArg[0]
		client_port = int(inputArg[1])
		inputArg = sys.argv[3].split(':')
		server_IP = inputArg[0]
		server_port = int(inputArg[1])
		return client_IP, client_port, server_IP, server_port

def start_connection(host, port):
    server_addr = (host, port)
    print('starting connection to', server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(msg_total=sum(len(m) for m in messages),
                                 recv_total=0,
                                 messages=list(messages),
                                 outb=b'')
    sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection')
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection')
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection')
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


###########################################################
messages = [b'Message 1 from client.', b'Message 2 from client.']

sel = selectors.DefaultSelector()
# ...
client_IP, client_port, server_IP, server_port = getInputArgs()
start_connection(server_IP, server_port)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            pass
        else:
            service_connection(key, mask)



