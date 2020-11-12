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
        fileName = input("Enter file name to send: ") #gets the filename from user
        file = open("./FilesToSend/" + fileName, "rb") 
        break
    except FileNotFoundError:
        print("File does not exist")

paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server) #split the server variable with the address and port
    serverPort = int(serverPort)  #convert port to intger
except:
    print("Can not parse server: port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET  #gets the address family(IPv4)
socktype = socket.SOCK_STREAM  #gets the type of scoket(TCP)
addrPort = (serverHost, serverPort) 

s = socket.socket(addrFamily,socktype)  #opens a socket

if s is None:
    print("could not open socket")
    sys.exit(1)

s.connect(addrPort) #establish a connection to the server

encapSock = EncapFramedSock((s,addrPort)) #creat a EncapFramesSock object with the socket to use it to encapsulate the contents of the file to send to the server where it will recieve it

fileContents = file.read() #get the file contents

if len(fileContents) == 0:
    print("File is empty, exit...")
    sys.exit(1)

print("sending filename")

encapSock.send(fileName,fileContents,debug)  #send the encapsulated file contents to server along with the file name
