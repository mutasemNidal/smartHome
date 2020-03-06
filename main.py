#!/usr/bin/env python3
import time
import netifaces as ni
from http.server import HTTPServer
from server import Server
import subprocess 
import os 
try: #get the ip address from specific interface
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
except:
    ni.ifaddresses('lo')
    ip = ni.ifaddresses('lo')[ni.AF_INET][0]['addr']
#intiate database
process = subprocess.run(["sqlite3 database.db < schema.sql"],shell=True,check=True, stdout=subprocess.PIPE, universal_newlines=True)
db_result=process.returncode
print("{}{}".format("\ndb intiate result is  ", db_result))
#server ip and port 
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