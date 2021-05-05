import socket
import time
import threading
import sys
import pickle
import os
from message import *
from logical_clock import *

class server():
    def __init__(self, server_id, host, port, clock):
        config = open("config",'r')
        configSplit = config.read().split("\n")
        config.close()
        self.server_id = server_id
        self.host = host
        self.middleware_port = int(configSplit[4].split('=')[1])
        self.port = port
        self.KVStore = {}
        self.clock = clock

    def serve(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.bind((self.host,self.port))
            print(f"server is listening on port {self.port}...")
            s.listen()
            conn,addr = s.accept()
            with conn:
                while True:
                    #Local Read Protocol
                    msg = pickle.loads(conn.recv(1024))
                    self.getClock().incrementClock()
                    their_clock = msg.getClock()
                    their_clock = self.updateClocks(their_clock)
                    if msg.getCmd() == "GET":
                        #print(f"Server is getting {msg.getPayload()}")
                        #print(f"Sending {self.get(msg.getPayload())}")
                        response = message("OK",self.get(msg.getPayload()),self.server_id,msg.getSender(),self.getClock())
                        conn.send(pickle.dumps(response))
                    elif msg.getCmd() == "SET":
                        self.totalOrderMulticast(msg)
                        response = message("OK","OK",self.server_id,msg.getSender(),self.getClock())
                        self.set(msg.getPayload())
                        conn.send(pickle.dumps(response))
                    elif msg.getCmd() == "BROADCAST":
                        their_clock = msg.getClock()
                        their_clock = self.updateClocks(their_clock)
                        response = message("ACK",None,self.server_id,msg.getSender(),self.getClock())

                        #I don't trust this set, this is why tests fail
                        self.set(msg.getPayload())
                        conn.send(pickle.dumps(response))

                    conn,addr = s.accept()

    def updateClocks(self, otherClock):
        self.clock.adjustClocks(otherClock)
        otherClock.adjustClocks(self.clock)
        return otherClock

    def get(self, key):
        return self.KVStore.get(key)

    def set(self, kv_tuple):
        self.KVStore.update({kv_tuple[0]:kv_tuple[1]})

    def totalOrderMulticast(self, msg):
        print("Total order multicast entered")
        key = msg.getPayload()[0]
        val = msg.getPayload()[1]
        broadcast = message("BROADCAST",(key,val),self.server_id,-1,self.getClock())
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1',self.middleware_port))
                s.send(pickle.dumps(broadcast))
            except ConnectionRefusedError:
                print("CONNECTION REFUSED DURING MULTICAST")

    def sendAcknowledgement(self,msg):
        print("Sending the acknowledgement!")
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1',self.middleware_port))
                s.send(pickle.dumps(msg))
            except ConnectionRefusedError:
                print("CONNECTION REFUSED DURING ACKNOWLEDGEMENT")

    def getClock(self):
        return self.clock


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 65432
    default_consistency = 'sequential'
    if len(sys.argv) >= 1:
        port = int(sys.argv[1])
        server_id = int(sys.argv[2])
    time.sleep(3)
    clock = logical_clock(server_id)
    s = server(server_id,host,port,clock)
    s.serve()

