import socket
import errno
import struct
import Queue
import logging

class client_info:
	_name = ''
	fin = 1
	ping = -1
	def __init__(self,s,cid):
		self.s = s
		self._name = "pughar"
		self.cid = cid

# Recieve the type of the next packet
def recv_header(s):
	type = -1
	fin = 1
	cid = -1
	try:

		#recieve the cid
		data = s.recv(2)
		if data == "" or len(data) != 2:
			print "Utter Failure!!!!!!!!!, why is it a bad header"
			return cid, fin, type
		cid = struct.unpack(">h",data)[0]

		# Try to recieve the type byte
		data = s.recv(2)

		if data == "":
			return fin, type

		fin = int(ord(data[0]))
		type = int(ord(data[1]))
	except socket.error, e:
		print "Error, hehehe, but it won't matter now"
	return cid, fin, type

# Handles packaging and unpackaging data for network packets
# ping, disconnect, minput, chat, error
class packager:
	send_queue = Queue.Queue()
	recv_queue = Queue.Queue()
	step = 0
	fin = 1

	def pack_minput(self,data):
		self.send_queue.put(struct.pack(">h2cc2i",c.cid,chr(self.fin),chr(2),data[0],data[1],data[2]))
	def unpack_minput(self,c):
		self.recv_queue.put((c.cid, self.step, 2))
		data = c.s.recv(9)
		if data == "" or len(data) != 9:
			print "didn't recieve all the data"
			return
		input_type, x, y = struct.unpack(">c2i",data)
		self.recv_queue.put((c.cid, self.step, 2, (input_type,x,y)))

	def pack_disconnect(self):
		pass
	def unpack_disconnect(self,c):
		pass

	def pack_ping(self,c):
		self.send_queue.put(struct.pack(">h2c",c.cid,chr(self.fin),chr(0)))
	def unpack_ping(self,c):
		#TODO: in order to calculate the ping accurately as soon as this is rx'd
		#      we need to send a pong back
		#print "got ping"
		self.recv_queue.put((c.cid, self.step, 0))

	def pack_chat(self,c,data):
		print data, "::", len(data)
		self.send_queue.put(struct.pack(">h2c"+"h"+str(len(data))+"s",c.cid,chr(self.fin),chr(3),len(data),data))
	def unpack_chat(self,c):
		print "chat message:"
		self.recv_queue.put((c.cid, self.step, 3, self.unpack_string(c)))

	def pack_name(self,c,data):
		self.send_queue.put(struct.pack(">h2c"+"h"+str(len(data))+"s",c.cid,chr(self.fin),chr(5),len(data),data))
	def unpack_name(self,c):
		self.recv_queue.put((c.cid, self.step, 5, self.unpack_string(c)))

	def pack_error(self,c,data):
		self.send_queue.put(struct.pack(">h2c"+"h"+str(len(data))+"s",c.cid,chr(self.fin),chr(4),len(data),data))
	def unpack_error(self,c):
		self.recv_queue.put((c.cid, self.step, 4, self.unpack_string(c)))

	def pack_nop(self,c):
		self.send_queue.put(struct.pack(">h2c",c.cid,chr(self.fin),chr(6)))
		#print "packing a nop with fin=" + str(self.fin)
	def unpack_nop(self,c):
		self.recv_queue.put((c.cid, self.step, 6))
		#print "got a nop"

	def pack_string(self,data):
		return struct.pack(">h"+str(len(data))+"s",len(data),data)
	def unpack_string(self,c):
		data = c.s.recv(2)
		if data == "" or len(data) != 2:
			return None
		size = struct.unpack(">h",data)[0]
		#print "size1 = " + str(size)
		data = c.s.recv(size)
		if data == "" or len(data) != size:
			return None
		#print "unpack_string = " + data
		d = struct.unpack(str(size)+"s",data)[0]
		print d
		return d

	unpack_map = {
		0 : unpack_ping,
		1 : unpack_disconnect,
		2 : unpack_minput,
		3 : unpack_chat,
		4 : unpack_error,
		5 : unpack_name,
		6 : unpack_nop
	}
