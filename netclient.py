import threading
import socket
import errno
from net import *
import logging

class client_thread(threading.Thread,packager):
	lock = threading.Lock()
	peerid = 0;
	_name = "player"  # apparently 'name' is already an instance method name of all classes....
	connected = False
	ping = False
	rtt = 0
	match = 1
	tron = 0

	def __init__(self,host,port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.s = socket.socket()
		self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.info = client_info(self.s,0)

	def recv(self):
		fin = 0
		print "Recieving data while not fin:"
		while not fin:
			'''
			if self.tron > 0:
				d = self.s.recv(2)
				print "SIZE=" + str(len(d))
			self.tron += 1
			'''

			cid, fin, type = recv_header(self.s)

			print "\tcid = " + str(cid) + ", fin = " + str(fin) + ", type = ", str(type)
			# Client disconnected so remove from the list
			if type == -1:
				print "Disconnected from server"
				self.s.close()
				connected = False

			else:
				# O(1) type lookup
				#TODO: need to add a try statement incase there is no map entry aka bad type
				self.unpack_map[type](self,self.info)

	def send(self):
		# The client has nothing to send so tell the server that :D
		if self.send_queue.empty():
			self.pack_nop(self.info)

		while not self.send_queue.empty():
			self.s.sendall(self.send_queue.get())

	def connect(self):
		try:
			self.s.connect((self.host,self.port))
			self.s.sendall(self.pack_string(self._name))

			#recieve the cid
			data = self.s.recv(2)
			if data == "" or len(data) != 2:
				print "Utter Failure!!!!!!!!!, not connected...."
				return None
			self.info.cid = struct.unpack(">h",data)[0]

			self.connected = True;
			print 'connected'
		except socket.error, e:
			print 'could not connect to server'

	def name(self,name):
		if self.connected:
			self.pack_name(self.info,name)

	def chat(self,data):
		if self.connected:
			self.pack_chat(self.info,data)

	def ping(self):
		if self.connected:
			self.pack_ping(self.info)
			ping = True

	def input(self):
		pass

	def disconnect(self):
		self.pack_disconnect(self.info)
		self.send()
		self.s.close()
		self.connected = False
