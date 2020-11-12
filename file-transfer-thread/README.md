File Transfer With Threading

To Run

First you have to run ./fileServer.py and then ./fileClient.py. Then input a
file name from the FilesToSend file to transfer. To run it with the proxy
provided, first run ./stammerProxy.py then run ./fileServer.py and lastly, run
./fileClient -s 127.0.0.1:50000

Details

If the file already exists in the RecievedFiles file the server will not
overwrite and just give a message that it already exists.

The Files Handled:
    - Zero length files
    - Large Files
    - Small Files
