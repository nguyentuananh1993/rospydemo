import socket
import cv2
import numpy
import sys
import threading

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

if __name__ == '__main__':	
    makeVideoRequest('127.0.0.1',)
