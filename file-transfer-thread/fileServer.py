#! /usr/bin/env python3

import sys
from encapFramedSock import EncapFramedSock

sys.path.append("../lib")
import re,socket,params,os

from threading import Thread,Lock

current_files = set()

lock = Lock()

def file_transfer_start(fname):
    global current_files,lock
    lock.acquire()
    if fname in current_files:
        print("File is currently being written to")
        lock.release()
        sys.exit(1)
    else:
        current_files.add(fname)
        lock.release()

def file_transfer_end(fname):
    global current_files,lock
    lock.acquire()
    current_files.remove(fname)
    lock.release()

switchesVarDefaults = (
    (('-l', '--listenPort'), "listenPort",50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addrToBind = ("127.0.0.1", listenPort)
lsock.bind(addrToBind)
lsock.listen(5)
print("listening on:", addrToBind)


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)

    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            payload = ""

            
            try:
                fileName, fileContents = self.fsock.receive(debug)
            except:
                print("File transfer failed")
                sys.exit(1)

            if debug: print("rec'd", payload)

            if payload is None:
                print("File contents were empty, exit...")
                sys.exit(1)

            fileName = fileName.decode()

            try:
                if not os.path.isfile("./RecievedFiles/" + fileName):
                    file_transfer_start(fileName)
                    file = open("./RecievedFiles/" + fileName, 'w+b')
                    file.write(fileContents)
                    file.close()
                    print("File", fileName, "accepted")
                    file_transfer_end(fileName)
                    sys.exit(0)
                else:
                    print("File with name", fileName, "already exits, exit...")
                    sys.exit(1)

            except FileNotFoundError:
                print("Fail")
                sys.exit(1)

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
