import net as N
import sys

if __name__ == '__main__':

	t = int(sys.argv[1])

	# Client
	if t:
		n = N.client_thread("localhost",8888)
		n.start()
		n.name("pughar")
	else:
		n = N.server_thread(8888)
		n.start()
