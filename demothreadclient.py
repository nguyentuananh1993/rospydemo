

import socket
import cv2
import numpy
import sys
import threading


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

def makeVideoRequest(cli, port=8002):
	TCP_IP = cli
	TCP_PORT = port
	sock = socket.socket()
	capture = cv2.VideoCapture(0)
	ret, frame = capture.read()
	sock.connect((TCP_IP, TCP_PORT))
	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
	while ret:
	    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
	    data = numpy.array(imgencode)
	    stringData = data.tostring()
	    sock.send( str(len(stringData)).ljust(16));
	    sock.send( stringData );
	    ret, frame = capture.read()
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
		a = getch()
		sock.send(a)
		if a=='n':
			sys.exit()
	sock.close()
if __name__ == '__main__':
	print 'Move by using w,a,s,d. press n to close.'
	threads = []
	t = threading.Thread(target=makeVideoRequest, args=("192.168.1.102",))
	t.setDaemon(True)
	threads.append(t)
	t.start()
	t = threading.Thread(target=makeRequest, args=("192.168.1.102",))
	threads.append(t)
	t.start()
