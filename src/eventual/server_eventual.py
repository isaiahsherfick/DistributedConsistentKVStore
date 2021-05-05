import socket
import time
import threading
import sys
import pickle
from message import *

class server():
    def __init__(self, host, port, default_consistency):
        self.host = host
        self.port = port
        self.consistency = default_consistency
        self.KVStore = {}
        self.server_information_dict = {}
        configFile = open("config", "r")
        configSplit = configFile.read().split('\n')[0:-1]
        self.top_level_controller_port = int(configSplit[4].split('=')[1])
        self.server_index = -1

    def blockUntilAcknowledgementReceived(self):
        pass
        #todo


    def fetchInfoFromTopLevelController(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1',self.top_level_controller_port))
                msg = s.recv(1024)
                self.server_information_dict = pickle.loads(msg)
                for i in self.server_information_dict:
                    if self.server_information_dict.get(i) == self.port:
                        self.server_index = i
                        break

            except ConnectionRefusedError:
                print("Connection refused. Did you run top_level_controller.py first?")

    #this is the method that runs assuming the system is eventual
    def handleClientEventual(self,conn, addr):
        msg = pickle.loads(conn.recv(1024))
        #print(f"Server #{self.server_index} heard {data}")
        cmd = msg.getCmd()
        if (cmd == "GET"):
            key = msg.getPayload()
            msg = message(self.get(key),self.get(key),None,None,None)
            conn.send(pickle.dumps(msg))
        elif (cmd == "SET"):
            key = msg.getPayload()[0]
            val = msg.getPayload()[1]
            self.set(key,val)
            ack = message("OK","OK",None,None,None)
            conn.send(pickle.dumps(ack))
            broadcastmsg = message("BROADCAST",(key,val),None,None,None)
            self.eventualBroadcast(broadcastmsg)
        elif (cmd == "BROADCAST"):
            key = msg.getPayload()[0]
            val = msg.getPayload()[1]
            self.set(key,val)
            ack = message("OK",None,None,None,None)
            conn.send(pickle.dumps(ack))

    def eventualBroadcast(self,msg):
        time.sleep(1)
        for i in self.server_information_dict:
            if self.server_information_dict.get(i) != self.port:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        #print(f"Broadcasting to {self.server_information_dict.get(i)}")
                        s.connect(('127.0.0.1',self.server_information_dict.get(i)))
                        s.send(pickle.dumps(msg))
                        acknowledgement_pickle = s.recv(1024)
                        acknowledgement = pickle.loads(acknowledgement_pickle)
                    except ConnectionRefusedError:
                        pass
            else:
                pass

    def get(self,key):
        return self.KVStore.get(key)

    def set(self,key,val):
        self.KVStore.update({key:val})

    def serve(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.bind((self.host,self.port))
            print(f"server is listening on port {self.port}...")
            s.listen()
            conn,addr = s.accept()
            with conn:
                while True:
                    if (self.consistency == 'eventual'):
                        t1 = threading.Thread(target=self.handleClientEventual,args=(conn,addr))
                        t1.start()
                        s.listen()
                        conn,addr = s.accept()
                    #Local Read Protocol
                    elif (self.consistency == 'sequential'):
                        data = pickle.loads(conn.recv(1024))
                        if data[0] == "GET":
                            conn.send(pickle.dumps(self.KVStore.get(data[1])))
                        elif data[0] == "SET":
                            self.totalOrderMulticast(msg)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 65432
    default_consistency = 'eventual'
    if len(sys.argv) >= 2:
        host = sys.argv[1]
        port = int(sys.argv[2])
    time.sleep(3)
    s = server(host,port,default_consistency)
    s.fetchInfoFromTopLevelController()
    s.serve()

