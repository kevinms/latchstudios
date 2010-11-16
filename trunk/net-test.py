import netclient as NC
import netserver as NS
import console as C
import sys
import time
import logging

# Enable/Disable Debug prints
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig()

# Run server: python net-test.py 0
# Run client: python net-test.py 1
# You can type chat messages into the client (eg. "say hello world")

def client():
	# Initialize components
	n = NC.client_thread(sys.argv[2],8888)
	n.connect()
	c = C.console(n)
	c.setDaemon(True)
	c.start()

	# Dummy main event loop for client
	while n.connected:
		if n.match:       # This loop will run at a pre determined rate (eg. 10 Hz)
			              # Pack/queue all player commands (NET:Provide methods to pack and queue)
			n.send()      # Send player commands           (NET:Provide method to send all packets)
			              # Process all commands           (NET:Provide access to all the commands)
			              # Process metrics                (NET:Provide access to simplified metrics)
			              # Progess turn number            (NET:Handle internally I think)
			time.sleep(1) # Dummy frame render time
			n.recv()     # Recv oponent commands          (NET:Provide method to recv all packets)
		else:
			pass

if __name__ == '__main__':
	t = int(sys.argv[1])

	# Client
	if t:
		client()
	# Server
	else:
		n = NS.server_thread(8888,3)
		n.start()
