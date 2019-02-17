# Python Selectors Library
# A simpler way to resemble async.
# Allows you to check for I/O completion on more than one socket.
# So you can call select() to see which sockets have I/O ready for reading and/or writing.

# This is an example of a server and client that address these problems.
# It uses select() to handle multiple connections simultaneously and call send() and recv() as many times as needed.


import selectors

def accept_wrapper(sock):
	conn, addr = sock.accept() # Should be ready to read.
	print('Accepted connection from', addr)
	conn.setblocking(False)
	data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	sel.register(conn, events, data=data)

# Client handles a connection when it's ready.
# arguments: key = the namedtuple returned from select(), mask = the events that are ready.
def service_connection(key, mask):
	sock = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		recv_data = sock.recv(1024) # Should be ready to read.
		if recv_data:
			data.outb += recv_data
		else:
			# This means the client has closed their socket, so the server should too.
			print('Closing connection to', data.addr)
			# Unregister it so it's no longer monitored by select()
			sel.unregister(sock)
			sock.close()
	if mask & selectors.EVENT_WRITE:
		if data.outb:
			print('Echoing', repr(data.outb), 'to', data.addr)
			sent = sock.send(data.outb) # Should be ready to write.
			data.outb = data.outb[sent:]



sel = selectors.DefaultSelector()

# Event Loop
while True:
	events = sel.select(timeout=None) # blocks until there are sockets ready for I/O. Returns a list of (key,event) tuples. One for each socket.
	for key, mask in events:
		if key.data is None:
			# We know it's from the listening socket and we should accept the connection.
			accept_wrapper(key.fileobj)
		else:
			# We know it's a client socket that's already been accepted, and we need to service it.
			service_connection(key, mask)

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))

# This is what makes the socket not block for each socket.
lsock.setblocking(False)

# Registers the socket to be monitored with sel.select() for the events we're interested in.
# For the listening socket, we want read events: selectors.EVENT_READ.
# data is used to store whatever arbitrary data you'd like along with the socket.
sel.register(lsock, selectors.EVENT_READ, data=None)