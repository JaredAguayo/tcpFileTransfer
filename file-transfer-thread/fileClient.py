#! /usr/bin/env python3

import socket,sys, re, os
from encapFramedSock import EncapFramedSock

sys.path.append("../lib")
import params

switchesVarDefaults = (
    (('-s', '--server'), "server", "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

while True:
    try:
        fileName = input("Enter file name to send: ")
        file = open("./FilesToSend/" + fileName, "rb")
        break
    except FileNotFoundError:
        print("File does not exist")

paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can not parse server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily,socktype)

if s is None:
    print("could not open socket")
    sys.exit(1)

s.connect(addrPort)

encapSock = EncapFramedSock((s,addrPort))

fileContents = file.read()

if len(fileContents) == 0:
    print("File is empty, exit...")
    sys.exit(1)

print("sending filename")

encapSock.send(fileName,fileContents,debug)
