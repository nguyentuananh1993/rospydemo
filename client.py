import socket
import cv2
import numpy
TCP_IP = 'localhost'
TCP_PORT = 8002
sock = socket.socket()
capture = cv2.VideoCapture(1)
ret, frame = capture.read()
sock.connect(("192.168.0.103", TCP_PORT))
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