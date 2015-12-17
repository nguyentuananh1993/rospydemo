import socket

TCP_IP = ''
TCP_PORT = 8003
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()
while 1:
	buf = conn.recv(1024)
	print buf
	if buf=='q':
		break;
s.close()
