import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def cameraVideoGet(cli = '', port = 8002):
    TCP_IP = cli
    TCP_PORT = port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(True)
    conn, addr = sock.accept()

    # camera
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

    while ret:
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        conn.send( str(len(stringData)).ljust(16));
        conn.send( stringData );
        ret, frame = capture.read()
        decimg=cv2.imdecode(data,1)
        cv2.imshow('SERVER',decimg)
        cv2.waitKey(10)
    s.close()
    cv2.destroyAllWindows() 

if __name__=="__main__":
    cameraVideoGet()


