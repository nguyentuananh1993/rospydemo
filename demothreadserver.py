#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys
import threading
import socket
import subprocess
import os
import numpy
import cv2

x_speed = 1

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()
    while 1:
        length = recvall(conn,16)
        stringData = recvall(conn, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        cv2.imshow('SERVER',decimg)
        cv2.waitKey(10)
    s.close()
    cv2.destroyAllWindows() 

def controlGet(cli = '', port = 8003):
    # initial socket
    TCP_IP = cli
    TCP_PORT = port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()

    rospy.init_node('move')
    p = rospy.Publisher('/turtle1/cmd_vel', Twist,queue_size=10)

    twist = Twist()
    twist.linear.x = 0;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = 0;                        # no rotation

    print "w a s d quit press n"
    while(1):

        mess = conn.recv(1024)
        if mess == 'w':
            twist.linear.x = x_speed
        elif mess == 's':
            twist.linear.x = -x_speed
        elif mess == 'a':
            twist.angular.z = x_speed
        elif mess == 'd':
            twist.angular.z = -x_speed
        elif mess == 'n':
            sys.exit()
        else:
            print 'Keep calm down and press slow!'

        for i in range(5):
            p.publish(twist)
            rospy.sleep(0.1) 
        twist = Twist()
        p.publish(twist)
    s.close()

if __name__=="__main__":
    threads = []
    t = threading.Thread(target=cameraVideoGet, args=())
    t.setDaemon(True)
    threads.append(t)
    t.start()
    controlGet()