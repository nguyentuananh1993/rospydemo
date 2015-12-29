import socket
import sys
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
        except KeyboardInterrupt:
        	sys.exit()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

TCP_IP = '127.0.0.1'
TCP_PORT = 8003
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((TCP_IP, TCP_PORT))
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
            socket.send('q')
            break
socket.close()