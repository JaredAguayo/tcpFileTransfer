#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import params,re,socket,os
from framedSock import framedSend,framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addrToBind = ("127.0.0.1", listenPort)
s.bind(addrToBind)
s.listen(5)
print("listening on:", addrToBind)
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)

    if not os.fork():
        print("connection rec'd from", addr)

        payload = ""

        try:
            fileName, fileContents = framedReceive(conn,debug)
        except:
            print("File transfer failed")
            sys.exit(1)

        if debug: print("rec'd: ", payload)

        if payload is None:
            print("File contents were empty, exit...")
            sys.exit(1)

        fileName = fileName.decode()

        try:
            if not os.path.isfile("./ReceivedFiles/" + fileName):
                file = open("./ReceivedFiles/" + fileName, 'w+b')
                file.write(fileContents)
                file.close()
                print("File", fileName, "accepted")
                sys.exit(0)
            else:
                print("File with name", fileName, "already exists, exit...")
                sys.exit(1)
        except FileNotFoundError:
            print("Fail")
            sys.exit(1)
