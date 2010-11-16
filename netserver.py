import threading
import socket
import select
import errno
import copy
from net import *

def find_client(client_list,conn):
	i = 0

	while i < len(client_list):
		if client_list[i].s == conn:
			return client_list[i]
		i += 1
	return None

def find_client_by_id(client_list,cid):
	i = 0

	while i < len(client_list):
		if client_list[i].cid == cid:
			return client_list[i]
		i += 1
	return None

class server_thread(threading.Thread,packager):
	client_list=[]
	lock = threading.Lock()
	power_lock = threading.Lock()

	def __init__(self,port,slots):
		threading.Thread.__init__(self)
		self.port = port
		self.slots = slots
		self.turn = 0

	def run(self):
		self.l = listen_thread(self.port,self.slots,self.client_list,self.power_lock,self.lock)
		self.l.setDaemon(True)
		self.l.start()

		self.l.acquire_lock()
		self.power_lock.acquire()

		while True:
			# Keep the server from eating up CPU cycles
			if not self.client_list:
				self.power_lock.release()
				self.l.acquire_lock()
				self.power_lock.acquire()

			self.recv()
			self.step += 1
			self.process()
			self.send()

	# Process all the data and get ready to send to the clients
	def process(self):
		while not self.recv_queue.empty():
			data = self.recv_queue.get()
			print "process " + str(data[0]) + str(data[1]) + str(data[2])
			if data[2] == 0:  # ping
				print "not sending out ping"
				continue;

			info = find_client_by_id(self.client_list,data[0])
			#print "type = " + str(data[2])

			if data[2] == 2:
				self.pack_input(info)
			elif data[2] == 1:
				self.pack_disconnect(info)
			elif data[2] == 0:
				self.pack_ping(info)
			elif data[2] == 3:
				self.pack_chat(info,data[3])
			elif data[2] == 5:
				self.pack_name(info,data[3])
			elif data[2] == 4:
				self.pack_error(info,data[3])
			elif data[2] == 6:
				print "processing nop"
				self.pack_nop(info)

			#packed_data = self.send_queue.queue.popleft()
			#print "str(len(packed_data)) = " + str(len(packed_data))
			#part = struct.pack(">h",data[0])
			#whole = struct.pack(str(len(part))+"s"+str(len(packed_data))+"s",part,packed_data)
			#self.send_queue.put(struct.pack(">"+str(len(packed_data))+"sh",packed_data,data[0]))

	# Send info to all clients to sync one turn
	def send(self):
		while not self.send_queue.empty():
			data = self.send_queue.get()
			for client in self.client_list:
				try:
					'''
					print "data================="
					print "datalen = " + str(len(data))
					print int(ord(data[0]))
					print int(ord(data[1]))
					print int(ord(data[2]))
					print int(ord(data[3]))
					print int(ord(data[4]))
					print int(ord(data[5]))
					'''

					client.s.sendall(data)
				except socket.error, e:
					print "Detected remote disconnect"
					self.client_list.remove(client)
					client.s.close()

	# Receive info from all clients for a single turn
	def recv(self):
		fd_set = [self.client_list[i].s for i in range(len(self.client_list))]

		while len(fd_set) > 0:
			inputt, outputt, exceptt = select.select(fd_set,[],[],5.0)

			if not inputt:
				print "TIMEOUT"  # DO SOMETHING ABOUT THIS!

			for s in inputt:
				c = find_client(self.client_list,s)
				self.parse(c)
				if c.fin:
					fd_set.remove(s)

	def parse(self,c):
		cid, fin, type = recv_header(c.s)
		c.fin = fin
		c.type = type

		# Client disconnected so remove from the list
		if type == -1:
			print "Removing client"
			c.s.close()
			self.lock.acquire()
			self.client_list.remove(c)
			self.lock.release()

		else:
			# O(1) type lookup
			#TODO: need to add a try statement incase there is no map entry aka bad type
			self.unpack_map[type](self,c)

	def ping(self):
		for client in self.client_list:
			try:
				client.c.send(data)
			except socket.error, e:
				print "Detected remote disconnect"
				self.client_list.remove(client)
				client.c.close()

# Thread to accept TCP connections from any client
class listen_thread(threading.Thread,packager):
	host = ''
	next_client_id = 2

	def __init__(self,port,slots,client_list,power_lock,lock):
		threading.Thread.__init__(self)
		self.port = port
		self.slots = slots
		self.client_list = client_list
		self.power_lock = power_lock
		self.lock = lock
		self.s = socket.socket()
		self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

	def run(self):
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.s.bind((self.host,self.port))
		self.s.listen(1)

		while True:
			c, addr = self.s.accept()
			c.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			if len(self.client_list) < self.slots:
				print addr
				info = client_info(c,self.next_client_id)
				info.s.sendall(struct.pack(">h",info.cid))
				self.next_client_id += 1
				info._name = self.unpack_string(info)
				if info._name == None:
					continue
				self.lock.acquire()
				self.client_list.append(info)
				print "connected"
				self.lock.release()
				self.power_lock.release()
			else:
				conn.send(self.pack_error("server full"))
	def acquire_lock(self):
		self.power_lock.acquire()
