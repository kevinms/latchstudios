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
		# recieve the cid
		data = s.recv(2)
		if data == "" or len(data) != 2:
			print "Utter Failure!!!!!!!!!, why is it a bad header"
			return cid, fin, type
		cid = struct.unpack(">h",data)[0]

		# recieve the fin and type bytes
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

	def pack_minput(self,c,data):
		p = struct.pack(">h2cc2i",                  # format string
		                c.cid,chr(self.fin),chr(2), # header
		                chr(data[0]),               # input_type
		                data[1],                    # x
		                data[2])                    # y

		self.send_queue.put(p)

	def unpack_minput(self,c,rx_cid):
		print "unpack_minput"
		# recieve the data
		data = c.s.recv(9)
		if data == "" or len(data) != 9:
			print "didn't recieve all the data"
			return
		# unpack the data
		input_type, x, y = struct.unpack(">c2i",data)

		p = (rx_cid, self.step, 2,  # general info
		    (int(ord(input_type)), # input_type
		    x,                     # x coordinate
		    y))                    # y coordinate

		self.recv_queue.put(p)

	def pack_disconnect(self,c):
		pass
	def unpack_disconnect(self,c,rx_cid):
		pass

	def pack_namechange(self,c):
		pass
	def unpack_namechange(self,c,rx_cid):
		pass

	def pack_addplayer(self,c):
		l = len(c._name)
		p = struct.pack(">h2ch"+"h"+str(l)+"s",     # format string
		                c.cid,chr(self.fin),chr(7), # header
		                c.cid,                      # id of new player
		                l,                          # len of name
		                c._name)                    # name of new player

		self.send_queue.put(p)

	def unpack_adduser(self,c,rx_cid):
		print "unpack_adduser"
		# recieve the cid
		data = c.s.recv(2)
		if data == "" or len(data) != 2:
			print "didn't recieve all the data"
			return
		# unpack the cid
		cid = struct.unpack(">h",data)

		# pack data into tuple and put on the queue
		p = (c.cid, self.step, 7,   # general info
		     cid,                   # new player cid
		     self.unpack_string(c)) # new player name

		self.recv_queue.put(p)

	def pack_delplayer(self,c):
		l = len(c._name)
		p = struct.pack(">h2ch",                    # format string
		                c.cid,chr(self.fin),chr(8), # header
		                c.cid)                      # id of del player

		self.send_queue.put(p)

	def unpack_deluser(self,c,rx_cid):
		print "unpack_deluser"
		# recieve the cid
		data = c.s.recv(2)
		if data == "" or len(data) != 2:
			print "didn't recieve all the data"
			return
		# unpack the cid
		cid = struct.unpack(">h",data)

		# pack data into tuple and put on the queue
		p = (c.cid, self.step, 8,   # general info
		     cid)                   # del player cid

		self.recv_queue.put(p)

	def pack_ping(self,c):
		p = struct.pack(">h2c",                     # format string
		                c.cid,chr(self.fin),chr(0)) # header

		self.send_queue.put(p)

	def unpack_ping(self,c,rx_cid):
		#TODO: in order to calculate the ping accurately as soon as
		#      this is rx'd we need to send a pong back
		p = (c.cid, self.step, 0) # general info

		self.recv_queue.put(p)

	def pack_chat(self,c,data):
		l = len(data)
		p = struct.pack(">h2c"+"h"+str(l)+"s",     # format string
		                c.cid,chr(self.fin),chr(3),# header
		                l,                         # len of chat message
		                data)                      # chat message string

		self.send_queue.put(p)

	def unpack_chat(self,c,rx_cid):
		print "chat message:"
		p = (c.cid, self.step, 3,   # general info
		     self.unpack_string(c)) # chat message string

		self.recv_queue.put(p)

	def pack_name(self,c,data):
		l = len(data)
		p = struct.pack(">h2c"+"h"+str(l)+"s",      # format string
		                c.cid,chr(self.fin),chr(5), # header
		                l,                          # len of name string
		                data)                       # name string

		self.send_queue.put(p)

	def unpack_name(self,c,rx_cid):
		p = (c.cid, self.step, 5,   # general info
		     self.unpack_string(c)) # name string

		self.recv_queue.put(p)

	def pack_error(self,c,data):
		l = len(data)
		p = struct.pack(">h2c"+"h"+str(l)+"s",     # format string
		                c.cid,chr(self.fin),chr(4),# header
		                l,                         # len of error string
		                data)                      # error string

		self.send_queue.put(p)

	def unpack_error(self,c,rx_cid):
		p = (c.cid, self.step, 4,   # general info
		     self.unpack_string(c)) # error string

		self.recv_queue.put(p)

	def pack_nop(self,c):
		p = struct.pack(">h2c",                     # format string
		                c.cid,chr(self.fin),chr(6)) # header

		self.send_queue.put(p)

	def unpack_nop(self,c,rx_cid):
		p = (c.cid, self.step, 6) # general info

		self.recv_queue.put(p)

	# data is a list of a list of players (e.g. [[cid,name],[cid,name]])
	def pack_players(self,data):
		'''
		l = len(data)
		player_str = 

		p = struct.pack(">h2ch"+str(l)+"s",         # format string
		                c.cid,chr(self.fin),chr(7), # header
		                l,                      # num of players
		                player_str)                 # packed player str

		self.send_queue.put(p)
		'''
	def unpack_players(self,c,rx_cid):
		pass

	def pack_string(self,data):
		return struct.pack(">h"+str(len(data))+"s", # format string
		                   len(data),               # string length
		                   data)                    # string data

	def unpack_string(self,c):
		# recieve the string length
		data = c.s.recv(2)
		if data == "" or len(data) != 2:
			return None
		size = struct.unpack(">h",data)[0]

		#recieve the string
		data = c.s.recv(size)
		if data == "" or len(data) != size:
			return None
		d = struct.unpack(str(size)+"s",data)[0]
		print d
		return d

	# set of function pointers mapped to the type number
	unpack_map = {
		0 : unpack_ping,
		1 : unpack_disconnect,
		2 : unpack_minput,
		3 : unpack_chat,
		4 : unpack_error,
		5 : unpack_name,
		6 : unpack_nop,
		7 : unpack_adduser,
		8 : unpack_deluser,
		9 : unpack_namechange
	}
