#!/usr/bin/python
 
import subprocess
import sys
import os.path
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
 
file=sys.argv[1]
 
def usage():
     print("Usage: " + sys.argv[0] + " <input file>\n")
 
def find(find, list):
    for i, val in enumerate(list):
        if val == find:
            return True
 
    return False
 
if not os.path.isfile(file):
     print("Error: Input file does not exist\n")
     usage()
     exit()
 
 
doc = ET.parse(file).getroot()
hosts = doc.findall('Report/ReportHost')
 
http_sockets = []
https_sockets = []
 
for host in hosts:
    items = host.findall('ReportItem')
    for item in items:
        if item.get('pluginName') == 'HTTP Server Type and Version':
            for tag in host.findall('HostProperties/tag'):
                if tag.attrib['name'] == 'host-ip':
                    socket = tag.text + ":" + item.get('port')
                    http_sockets.append(socket)
 
for host in hosts:
    items = host.findall('ReportItem')
    for item in items:
        if item.get('pluginName') == 'SSL / TLS Versions Supported':
            for tag in host.findall('HostProperties/tag'):
                if tag.attrib['name'] == 'host-ip':
                    socket = tag.text + ":" + item.get('port')
                    if find(socket, http_sockets):
                        https_sockets.append(socket)
                             
 
for socket in http_sockets:
    if not find(socket, https_sockets):
        print("http://" + socket)
        http_socket = ("http://" + socket)
        subprocess.run(['dirb', socket])
 
for socket in https_sockets:
    print("https://" + socket)
    https_socket = ("http://" + socket)
    subprocess.run(['dirb', https_socket])
   
