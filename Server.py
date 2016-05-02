import threading
import socket
import struct
import time

class Server(threading.Thread):
    client=0

    def __init__(self, client):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.client=client

    def run(self):
        while True:
            print(self.client)
            self.client+=1
            time.sleep(1)
