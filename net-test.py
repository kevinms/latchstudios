import net as N
import sys
import time

# Run server: python net-test.py 0
# Run client: python net-test.py 1
# You can type chat messages into the client

if __name__ == '__main__':

	t = int(sys.argv[1])

	# Client
	if t:
		n = N.client_thread("localhost",8888)
		n.connect()
		#time.sleep(2)
		#n.name("pughar")
		while 1:
			s = sys.stdin.readline()
			n.chat(s.strip())
	# Server
	else:
		n = N.server_thread(8888,2)
		n.start()
