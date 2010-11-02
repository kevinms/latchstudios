import socket
import errno
import struct
import Queue

# Recieve the type of the next packet
def recv_header(s):
	type = -1
	fin = 1
	try:
		# Try to recieve the type byte
		data = s.recv(2)

		if data == "":
			return fin, type

		fin = int(ord(data[0]))
		type = int(ord(data[1]))
	except socket.error, e:
		print "Error, hehehe, but it won't matter now"
	return fin, type

# Handles packaging and unpackaging data for network packets
# ping, disconnect, input, chat, error
class packager():
	send_queue = Queue.Queue()
	recv_queue = Queue.Queue()
	turn = 0
	fin = 1

	def pack_input(self):
		pass
	def unpack_input(self,s):
		pass

	def pack_disconnect(self):
		pass
	def unpack_disconnect(self,s):
		pass

	def pack_ping(self):
		self.send_queue.put(struct.pack(">2c",chr(self.fin),chr(0)))
	def unpack_ping(self,s):
		#TODO: in order to calculate the ping accurately as soon as this is rx'd
		#      we need to send a pong back
		print "got ping"
		self.recv_queue.put(self.fin, 0)

	def pack_chat(self,data):
		self.send_queue.put(struct.pack(">2c"+"h"+str(len(data))+"s",chr(self.fin),chr(3),len(data),data))
	def unpack_chat(self,s):
		print "chat message:"
		self.recv_queue.put(self.turn, 3, self.unpack_string(s))

	def pack_name(self,data):
		self.send_queue.put(struct.pack(">2c"+"h"+str(len(data))+"s",chr(self.fin),chr(5),len(data),data))
	def unpack_name(self,s):
		self.recv_queue.put(self.turn, 5, self.unpack_string(s))

	def pack_error(self,data):
		self.send_queue.put(struct.pack(">2c"+"h"+str(len(data))+"s",chr(self.fin),chr(4),len(data),data))
	def unpack_error(self,s):
		self.revc_queue.put(self.turn, 4, self.unpack_string(s))

	def unpack_string(self,s):
		size = struct.unpack(">h",s.recv(2))[0]
		data = s.recv(size)
		d = struct.unpack(str(size)+"s",data)[0]
		print d
		return d

	unpack_map = {
		0 : unpack_ping,
		1 : unpack_disconnect,
		2 : unpack_input,
		3 : unpack_chat,
		4 : unpack_error,
		5 : unpack_name
	}
