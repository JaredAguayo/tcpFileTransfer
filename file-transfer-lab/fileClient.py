#! /usr/bin/env python3

import socket, sys, re,os

sys.path.append("../lib")
import params
from framedSock import framedSend,framedReceive

switchesVarDefaults = (
    (('-s', '--server'), "server", "127.0.0.1:50001"),
    (('-d', '--debug'), "debug",False),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

while True:
    try:
        fileName = input("Enter File Name\n")
        file = open("./FilesToTest/" + fileName,"rb")
        break
    except FileNotFoundError:
        print("File does not exist, please enter another file name")

paramMap = params.parseParams(switchesVarDefaults)
server, usage,debug  = paramMap["server"], paramMap["usage"],paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

fileContents = file.read()

if len(fileContents) == 0:
    print("File Empty, exit...")
    sys.exit(1)

print("sending file")

framedSend(s,fileName,fileContents,debug)
