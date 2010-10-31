import threading
import socket
import select
import errno
import struct
import time

# Handles packing and unpacking data for network packets
class packet():
	def pack_input(self,s):
		pass
	def unpack_input(self,s):
		pass

	def unpack_disconnect(self,s):
		pass

	def pack_ping(self):
		return struct.pack(">c",chr(0));
	def unpack_ping(self,s):
		print 'ping'

	def pack_chat(self,data):
		return struct.pack(">c"+"h"+str(len(data))+"s",chr(3),len(data),data)
	def unpack_chat(s):
		size = struct.unpack(">h",s.recv(2))[0]
		data = s.recv(size)
		tmp = struct.unpack(str(size)+"s",data)[0]
		print tmp
		return tmp

	def pack_error(self,data):
		return struct.pack(">c"+"h"+str(len(data))+"s",chr(4),len(data),data)
	def unpack_error(self,s):
		size = struct.unpack(">h",s.recv(2))[0]
		data = s.recv(size)
		tmp = struct.unpack(str(size)+"s",data)[0]
		print tmp
		return tmp

	unpack_map = {
		0 : unpack_ping,
		1 : unpack_disconnect,
		2 : unpack_input,
		3 : unpack_chat,
		4 : unpack_error
	}

class client_thread(threading.Thread,packet):
	lock = threading.Lock()
	peerid = 0;
	name = ''
	connected = False

	def __init__(self,host,port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.s = socket.socket()
		self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		
	def connect(self):
		# Connect to the server
		try:
			self.s.connect((self.host,self.port))
			self.connected = True;
			print 'hello world'
		except socket.error, e:
			print 'could not connect to server'

	def name(self,name):
		if self.connected:
			self.name = name
			self.s.send(self.name)

	def chat(self,data):
		if self.connected:
			self.s.send(self.pack_chat(data))

	def synch_state(self):
		print "LOL, riiiiight....."

	def ping(self):
		if self.connected:
			self.s.send(self.pack_ping())

	def run(self):
		self.connect()
		while 1:
			pass

class server_thread(threading.Thread,packet):
	client_list=[]
	lock = threading.Lock()

	def __init__(self,port,slots):
		threading.Thread.__init__(self)
		self.port = port
		self.slots = slots

	def run(self):
		self.l = listen_thread(self.port,self.slots,self.client_list,self.lock)
		self.l.start()
		
		while True:
			inputt, outputt, exceptt = select.select(self.client_list,[],[],0.5)
			for s in inputt:
				self.parse(s)

	def parse(self,s):
		data = ""
		try:
			# Try to recieve the type byte
			data=s.recv(1)
		except socket.error, e:
			print "Error, hehehe, but it won't matter now"
			return
		
		# Client disconnected so remove from the list
		if data == "":
			print "Removing client"
			self.lock.acquire()
			self.client_list.remove(s)
			self.lock.release()
			s.close()

		else:
			# O(1) type lookup
			#TODO: need to add a try statement incase there is no map entry aka bad type
			i = ord(data)
			self.unpack_map[i](s)
"""
		else:
			print data.strip()
			
			self.lock.acquire()
			for client in self.client_list:
				if client is not s:
					try:
						client.send(data)
					except socket.error, e:
						print "Detected remote disconnect"
						self.client_list.remove(client)
						client.close()
			self.lock.release()
"""

# Thread to accept TCP connections from any client
class listen_thread(threading.Thread,packet):
	host = ''
	def __init__(self,port,slots,client_list,lock):
		threading.Thread.__init__(self)
		self.port = port
		self.slots = slots
		self.client_list = client_list
		self.lock = lock
		self.s = socket.socket()
		self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

	def run(self):
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.s.bind((self.host,self.port))
		self.s.listen(1)

		while True:
			conn, addr = self.s.accept()
			conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			if len(self.client_list) < self.slots:
				print addr
				self.lock.acquire()
				self.client_list.append(conn)
				self.lock.release()
			else:
				conn.send(self.pack_error("server full"))
