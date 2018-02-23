import socket
import sys
from time import sleep

x = 0
y = 0
while True:
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect the socket to the port where the server is listening
	server_address = ('localhost', 8888)

	try:
		sock.connect(server_address)
		message = str(x) + " " + str(y)
		sock.sendall(message)
		x += 5
		y += 5
		if x >= 200:
			x = 0
			y = 0
	except:
		pass

	 
	

	sleep(0.1)