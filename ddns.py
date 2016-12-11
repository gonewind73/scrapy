#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created on 2016年8月17日

@author: heguofeng

在系统中 运行
'''

import socket
import fcntl
import struct
import requests
import re
import time
  
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
  

if __name__ == '__main__':
    time.sleep(10)
    oldlocalwlanip=""
    oldlocaleth0ip=""
    oldip138=""
    while True:
        localwlanip=""
        localeth0ip=""
        ip138=""
        try:
            localwlanip = get_ip_address(b'wlan0');
            localeth0ip = get_ip_address(b'eth0');
            ip138=re.findall(r"\[.+\]",requests.get("http://1212.ip138.com/ic.asp").text)[0][1:-1]
            
            if ((localwlanip!=oldlocalwlanip) or (oldip138!=ip138) or (localeth0ip!=oldlocaleth0ip)):
                file=open("/tmp/ddns.log","w");
                file.write(localwlanip);
                file.write(localeth0ip);
                file.write(ip138);
                file.close();
                print(localwlanip,localeth0ip,ip138)
                oldlocaleth0ip=localeth0ip
                oldip138=ip138
                oldlocalwlanip=localwlanip
                r=requests.post("http://gonewind.pythonanywhere.com/postip",
                            {"wlanip":localwlanip,"138ip":ip138,"eth0ip":localeth0ip});
                time.sleep(300)
        except:
            r=requests.post("http://gonewind.pythonanywhere.com/postip",
                            {"wlanip":localwlanip,"138ip":ip138,"eth0ip":localeth0ip});
            time.sleep(3600)

    
    