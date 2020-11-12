#! /usr/bin/env python3

import sys
from encapFramedSock import EncapFramedSock

sys.path.append("../lib")
import re,socket,params,os

from threading import Thread,Lock

current_files = set()  #creates a set to add filenames and remove file names from

lock = Lock() #create the lock 

def file_transfer_start(fname):
    global current_files,lock  
    lock.acquire()   #acquire lock since you may need to alter global variables
    if fname in current_files:
        print("File is currently being written to")
        lock.release() #release the lock if the file is already in the set
        sys.exit(1)
    else:
        current_files.add(fname) #add the file to the set 
        lock.release() #release the lock

def file_transfer_end(fname):
    global current_files,lock
    lock.acquire()   #aquire the lock 
    current_files.remove(fname)   #remove the file from the set 
    lock.release()  #release the lock

switchesVarDefaults = (
    (('-l', '--listenPort'), "listenPort",50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creates a listener socket
addrToBind = ("127.0.0.1", listenPort)   #putting the address and port together for the bind
lsock.bind(addrToBind)    #binding the listener socket to the specific address and port that can be used to listen to incoming requests on those specific address and port
lsock.listen(5)   #set the socket to listen to incoming connections, set to listen for up to 5
print("listening on:", addrToBind) 


class Server(Thread):   #create a class for threads for each incoming connection
    def __init__(self, sockAddr):  #takes the socket and address tuple returned from .accept()
        Thread.__init__(self)
        self.sock, self.addr = sockAddr   #putting the tuple into seperate variables
        self.fsock = EncapFramedSock(sockAddr)  #create an object from EncapFramedSock to recieve an EncapFramedSock message from the client

    def run(self):
        print("new thread handling connection from", self.addr) 
        while True:  
            payload = "" 
            
            try:
                fileName, fileContents = self.fsock.receive(debug)   #gets the filename and whats in the file from using the recieve method from EncapFramedSock
            except:
                print("File transfer failed")
                sys.exit(1)

            if debug: print("rec'd", payload)

            if payload is None: 
                print("File contents were empty, exit...")
                sys.exit(1)

            fileName = fileName.decode()  

            try:
                if not os.path.isfile("./RecievedFiles/" + fileName):  #if the file doesnt already exist 
                    file_transfer_start(fileName)
                    file = open("./RecievedFiles/" + fileName, 'w+b')  #opens a new file
                    file.write(fileContents)  #writes to the file
                    file.close()  #closes it
                    print("File", fileName, "accepted")
                    file_transfer_end(fileName)   
                    sys.exit(0)
                else:       #if the file already exists it just exits
                    print("File with name", fileName, "already exits, exit...")
                    sys.exit(1)

            except FileNotFoundError:
                print("Fail")
                sys.exit(1)

while True:   #infinite loop to accept connections and create a new thread ffor each new connection
    sockAddr = lsock.accept()    #blocks and waits for incoming connections and gets the new socket representing the connection and the address of the client
    server = Server(sockAddr)    #creates a new thread once it accepts the connection
    server.start()    #start the thread
