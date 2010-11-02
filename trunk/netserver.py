import threading
import socket
import select
import errno
from net import *

class server_thread(threading.Thread,packager):
	client_list=[]
	lock = threading.Lock()

	def __init__(self,port,slots):
		threading.Thread.__init__(self)
		self.port = port
		self.slots = slots

	def run(self):
		self.l = listen_thread(self.port,self.slots,self.client_list,self.lock)
		self.l.setDaemon(True)
		self.l.start()
		
		while True:
			inputt, outputt, exceptt = select.select(self.client_list,[],[],0.5)
			for s in inputt:
				self.parse(s)

	def parse(self,s):
		fin, type = recv_header(s)

		# Client disconnected so remove from the list
		if type == -1:
			print "Removing client"
			self.lock.acquire()
			self.client_list.remove(s)
			self.lock.release()
			s.close()

		else:
			# O(1) type lookup
			#TODO: need to add a try statement incase there is no map entry aka bad type
			self.unpack_map[type](self,s)

	def sync_state(self):
		for client in self.client_list:
			try:
				client.send(data)
			except socket.error, e:
				print "Detected remote disconnect"
				self.client_list.remove(client)
				client.close()

# Thread to accept TCP connections from any client
class listen_thread(threading.Thread,packager):
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
