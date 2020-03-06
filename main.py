#!/usr/bin/env python3
import time
import netifaces as ni
from http.server import HTTPServer
from server import Server
import socket
import fcntl
import struct
eth_interface= 'etho'
lo_interface='lo'
try:
    ni.ifaddresses('eht0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
except:
    ni.ifaddresses('lo')
    ip = ni.ifaddresses('lo')[ni.AF_INET][0]['addr']
    
print(ip ) # should print "192.168.100.37"
HOST_NAME = ip
PORT_NUMBER = 8000
if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))