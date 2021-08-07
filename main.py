#!/usr/bin/env python3
import time
import netifaces as ni
from http.server import HTTPServer
from server import Server
import subprocess 
import os 
import asyncio
from xknx import XKNX
from xknx.devices import Light
from xknx.io import GatewayScanner
from xknx.telegram import AddressFilter

print(ni.interfaces())
try: #get the ip address from specific interface
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
except:
    ni.ifaddresses('lo')
    ip = ni.ifaddresses('lo')[ni.AF_INET][0]['addr']
#intiate database
#process = subprocess.run(["sqlite3 database.db < schema.sql"],shell=True,check=True, stdout=subprocess.PIPE, universal_newlines=True)
#db_result=process.returncode
#print("{}{}".format("\ndb intiate result is  ", db_result))
#server ip and port 
HOST_NAME = ip
PORT_NUMBER = 80
if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        async def main():
            xknx = XKNX()
            gatewayscanner = GatewayScanner(xknx)
            gateways = await gatewayscanner.scan()
			
            if not gateways:
                print("No Gateways found")

            else:
                for gateway in gateways:
                    print("Gateway found: {0} / {1}:{2}".format(
                        gateway.name,
                        gateway.ip_addr,
                        gateway.port))
                    if gateway.supports_tunnelling:
                        print("- Device supports tunneling")
                        await xknx.start()
                        light = Light(xknx,
                        name='TestLight',
                        group_address_switch='0/1/1')
                        print("im here")
                        await light.set_on()
                        await asyncio.sleep(9)
                        await light.set_off()
                        await xknx.stop()

                    if gateway.supports_routing:
                        print("- Device supports routing, connecting via {0}".format(
                            gateway.local_ip))

         # pylint: disable=invalid-name
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
        print("hello world")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
   
