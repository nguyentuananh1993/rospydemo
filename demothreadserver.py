#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import MotorPower
import sys
import threading
import socket
import subprocess
import os
import numpy
import cv2
import select
import time

x_speed = 0.2

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
    sock.close()
    cv2.destroyAllWindows() 

    
def controlGet(cli = '', port = 8003):
    # initial socket
    TCP_IP = cli
    TCP_PORT = port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)
    while 1:
        conn, addr = s.accept()
        print '- Client '+str(addr)+' just connect.'
        rospy.init_node('CutiesNode')
        p = rospy.Publisher('/mobile_base/commands/velocity', Twist,queue_size = 10)
        while(1):    
            twist = Twist()
            twist.linear.x = 0;                         # our forward speed
            twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
            twist.angular.x = 0; twist.angular.y = 0;   #          or these!
            twist.angular.z = 0;                        # no rotation
            try:
                mess = conn.recv(1)
                # print mess
            except:
                print 'Auto disconnect to client:' + str(addr)
                break
            if mess == 'w':
                twist.linear.x = x_speed
                print '[ INFO] ['+str(rospy.get_time())+'] KeyOp: linear Velocity incremented [0.2|0]'
            elif mess == 's':
                twist.linear.x = -x_speed
                print '[ INFO] ['+str(rospy.get_time())+'] KeyOp: linear Velocity decremented [0.2|0]'
            elif mess == 'a':
                twist.angular.z = x_speed*2
                print '[ INFO] ['+str(rospy.get_time())+'] KeyOp: angular Velocity incremented [0|0.4]'
            elif mess == 'd':
                twist.angular.z = -x_speed*2
                print '[ INFO] ['+str(rospy.get_time())+'] KeyOp: angular Velocity decremented [0|-0.4]'
            elif mess == 'e':
                sys.exit()
            else:
                print 'Wrong key.'
            for i in range(0, 2):
                p.publish(twist)
                rospy.sleep(0.2) 
    s.close()

if __name__=="__main__":
    # threads = []
    # t = threading.Thread(target=cameraVideoGet, args=())
    # t.setDaemon(True)
    # threads.append(t)
    # t.start()
    controlGet()
