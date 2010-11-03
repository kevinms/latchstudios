import threading
import socket
import errno
from net import *

class client_thread(threading.Thread,packager):
	lock = threading.Lock()
	peerid = 0;
	_name = "player"  # apparently 'name' is already an instance method name of all classes....
	connected = False
	ping = False
	rtt = 0
	match = 1

	def __init__(self,host,port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.s = socket.socket()
		self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

	def recv(self):
		fin = 0
		self.turn += 1

		while not fin:
			fin, type = recv_header(self.s)

			# Client disconnected so remove from the list
			if type == -1:
				print "Disconnected from server"
				self.s.close()
				connected = False

			else:
				# O(1) type lookup
				#TODO: need to add a try statement incase there is no map entry aka bad type
				self.unpack_map[type](self,self.s)

	def send(self):
		# The client has nothing to send so tell the server that :D
		if self.send_queue.empty():
			self.pack_nop()

		while not self.send_queue.empty():
			self.s.sendall(self.send_queue.get())

	def connect(self):
		try:
			self.s.connect((self.host,self.port))
			self.s.sendall(self.pack_string(self._name))
			self.connected = True;
			print 'hello world'
		except socket.error, e:
			print 'could not connect to server'

	def name(self,name):
		if self.connected:
			self.pack_name(name)

	def chat(self,data):
		if self.connected:
			self.pack_chat(data)

	def ping(self):
		if self.connected:
			self.pack_ping()
			ping = True

	def input(self):
		pass

	def disconnect(self):
		self.pack_disconnect()
		self.send()
		self.s.close()
		self.connected = False
