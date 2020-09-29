#! /usr/bin/env python3

import socket, sys, re
from sockHelpers import sendAll

sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

conn, addr = s.accept() # wait until incoming connection request (and accept it)

print('Connected by', addr)

text_file = 'serverRecNorm.txt'

with open (text_file,'w') as writeFile:
    trans = conn.recv(1024).decode()
    for recieve in trans:
        print(recieve)
        writeFile.write(recieve)

conn.close()
        
