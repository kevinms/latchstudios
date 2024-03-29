import threading
import socket
import select
import errno
import copy
from net import *
import logging
import time

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
	
	# so the server can act like a client
	psuedo_client = client_info(None,0)
	psuedo_client._name = "server"

	def __init__(self,port,slots,bench):
		threading.Thread.__init__(self)
		self.port = port
		self.slots = slots
		self.turn = 0
		self.frames = 0
		self.timedelta = time.time()
		self.frametime = 0
		self.benchmark = bench

	def run(self):
		self.l = listen_thread(self.port,self.slots,self.client_list,self.psuedo_client,self.power_lock,self.lock)
		self.l.setDaemon(True)
		self.l.start()

		self.l.acquire_lock()
		self.power_lock.acquire()

		logging.debug('===============================')

		while True:
			# Keep the server from eating up CPU cycles
			if (self.client_list) == 0:
				self.power_lock.release()
				self.l.acquire_lock()
				self.power_lock.acquire()

			self.timedelta = time.time()

			self.recv()
			self.step += 1
			self.process()
			self.send()

			if self.benchmark:
				self.frametime += (time.time() - self.timedelta)
				self.timedelta = time.time()
				self.frames += 1
				if self.frametime > 1:
					print "FPS: " + str(self.frames/self.frametime)
					self.frametime = 0.0
					self.frames = 0

	# Process all the data and get ready to send to the clients
	def process(self):
		self.fin = 0
		while not self.recv_queue.empty():
			data = self.recv_queue.get()
			logging.debug("process: " + str(data[0]) + " " + str(data[1]) + " " + str(data[2]))
			if data[2] == 0:  # ping
				print "not sending out ping"
				continue;

			info = find_client_by_id(self.client_list,data[0])
			#print "type = " + str(data[2])

			if data[2] == 2:
				self.pack_minput(info,data[3])
			elif data[2] == 1:
				self.pack_disconnect(info)
			elif data[2] == 0:
				self.pack_ping(info)
			elif data[2] == 3:
				logging.debug("packing it now")
				self.pack_chat(info,data[3])
			elif data[2] == 5:
				self.pack_name(info,data[3])
			elif data[2] == 4:
				self.pack_error(info,data[3])
			elif data[2] == 6: # ignore this :D (optimization)
				#print "processing nop"
				#self.pack_nop(info)
				pass

		# pack up a single nop from the server to let the clients know
		# the step is over
		self.fin = 1
		self.pack_nop(self.psuedo_client)

	# Send info to all clients to sync one turn
	def send(self):
		logging.debug("Sending all data:")
		dropped_client_list = []

		while not self.send_queue.empty():
			data = self.send_queue.get()
			logging.debug("\tGetting data to send:")
			for client in self.client_list:
				try:
					logging.debug("\t\tTrying to print data")
					l = len(data)
					logging.debug(str(l))
					logging.debug("\t\t" + str(int(ord(data[0]))))
					logging.debug("\t\t" + str(int(ord(data[1]))))
					logging.debug("\t\t" + str(int(ord(data[2]))))
					logging.debug("\t\t" + str(int(ord(data[3]))))
					client.s.sendall(data)
				except socket.error, e:
					print "Detected remote disconnect"
					dropped_client_list.append(client)
					self.client_list.remove(client)
					client.s.close()
		# Do this outside the loop because we don't want to mess up the
		# send_queue which has the last packet's fin bit = 1
		for client in dropped_client_list:
			self.pack_delplayer(client)

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
		#print "grep: " + str(c.cid)

		# Client disconnected so remove from the list
		if type == -1:
			print "Removing client"
			self.pack_delplayer(c)
			c.s.close()
			self.lock.acquire()
			self.client_list.remove(c)
			self.lock.release()

		else:
			# O(1) type lookup
			#TODO: need to add a try statement incase there is no map entry aka bad type
			self.unpack_map[type](self,c,cid)

	def ping(self):
		for client in self.client_list:
			try:
				client.c.send(data)
			except socket.error, e:
				print "Detected remote disconnect"
				self.pack_delplayer(c)
				self.client_list.remove(client)
				client.c.close()

# Thread to accept TCP connections from any client
class listen_thread(threading.Thread,packager):
	host = ''
	next_client_id = 1

	def __init__(self,port,slots,client_list,psuedo_client,power_lock,lock):
		threading.Thread.__init__(self)
		self.port = port
		self.slots = slots
		self.client_list = client_list
		self.psuedo_client = psuedo_client
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

				# tell new player cid/name of other players
				client_cid_name_list = []
				print "len(client_list)=%d" % len(self.client_list)
				for client in self.client_list:
					client_cid_name_list.append([client.cid,client._name])
				p = self.pack_players(self.psuedo_client,client_cid_name_list)


				info.s.sendall(p)

				self.lock.acquire()
				self.client_list.append(info)
				print "connected"
				self.lock.release()
				
				if len(self.client_list) == 1:
					self.power_lock.release()

				# update all players notifying them of a new client
				self.pack_adduser(info)
			else:
				conn.send(self.pack_error("server full"))
	def acquire_lock(self):
		self.power_lock.acquire()
