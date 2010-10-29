import threading
import socket
import select
import errno

class client_thread(threading.Thread):
	lock = threading.Lock()
	peerid = 0;
	name = ''
	connected = False

	def __init__(self,host,port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.s = socket.socket()
		
	def connect(self):
		print 'hello world'
		
		# Connect to the server
		self.s.connect((self.host,self.port))
		self.connected = True;
	
	def name(self,name):
		if self.connected:
			self.name = name
			self.s.send(self.name)

	def synch_state(self):
		print "LOL, riiiiight....."

	def run(self):
		self.connect()

class server_thread(threading.Thread):
	client_list=[]
	lock = threading.Lock()

	def __init__(self,port):
		threading.Thread.__init__(self)
		self.port = port

	def run(self):
		self.l = listen_thread(self.port,self.client_list,self.lock)
		self.l.start()
		
		while True:
			inputt, outputt, exceptt = select.select(self.client_list,[],[],0.5)
			for s in inputt:
				self.parse(s)

	def parse(self,s):
		data = ""
		try:
			data=s.recv(1024)
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

# Thread to accept TCP connections from any client
class listen_thread(threading.Thread):
	host = ''
	def __init__(self,port,client_list,lock):
		threading.Thread.__init__(self)
		self.port = port
		self.client_list = client_list
		self.lock = lock
		self.s = socket.socket()

	def run(self):
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.s.bind((self.host,self.port))
		self.s.listen(1)

		while True:
			conn, addr = self.s.accept()
			print addr
			self.lock.acquire()
			self.client_list.append(conn)
			self.lock.release()
