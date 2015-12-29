

import socket
import cv2
import numpy
import sys
import threading
import msvcrt

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character. 
        Nothing is echoed to the console. This call will block if a keypress 
        is not already available, but will not wait for Enter to be pressed. 

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def makeVideoRequest(cli, port=8002):
    TCP_IP = cli
    TCP_PORT = port
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))

    while 1:
        length = recvall(sock,16)
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        cv2.imshow('CLIENT',decimg)
        cv2.waitKey(10)
    sock.close()
    cv2.destroyAllWindows() 


def makeRequest(cli, port=8003):
	TCP_IP = cli
	TCP_PORT = port
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((TCP_IP, TCP_PORT))
	while 1:
		if msvcrt.kbhit():
        keypress = ord(msvcrt.getch())
        if keypress == 119 or keypress == 72:
            print 'up'
            socket.send('w')
        if keypress == 115 or keypress == 80:
            print 'down'
            socket.send('s')
        if keypress == 97 or keypress == 75:
            print 'left'
            socket.send('a')
        if keypress == 100 or keypress == 77:
            print 'right'
            socket.send('d')
        if keypress == 101:
            print 'stop'
            socket.send('e')
			sys.exit()
	sock.close()
if __name__ == '__main__':
	ipadds = '192.168.43.97'
	print 'Move by using w,a,s,d. press e to close.'
	threads = []
	t = threading.Thread(target=makeVideoRequest, args=(ipadds,))
	t.setDaemon(True)
	threads.append(t)
	t.start()
	t = threading.Thread(target=makeRequest, args=(ipadds,))
	threads.append(t)
	t.start()
