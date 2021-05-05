import socket
import random
import sys
import time
import pickle
from message import *

HOST = '127.0.0.1'
PORT = 65432

class client:
    def __init__(self):
        self.server_information_dict = {}
        configFile = open("config",'r')
        configSplit = configFile.read().split('\n')[0:-1]
        configFile.close()
        self.top_level_controller_port = int(configSplit[4].split('=')[1])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1',self.top_level_controller_port))
                msg = s.recv(1024)
                self.server_information_dict = pickle.loads(msg)
            except ConnectionRefusedError:
                print("Client could not connect to top level controller.")
                print(f"Top level controller port: {self.top_level_controller_port}")

    def sendRequest(self, msg, server_index,return_array):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port = self.server_information_dict.get(server_index)
            try:
                s.connect(('127.0.0.1',port))
                s.send(pickle.dumps(msg))
                response = s.recv(1024)
                try:
                    data = pickle.loads(response).getPayload()
                    return_array += [data]
                    return data
                except EOFError:
                    return "CONNECTION INTERRUPTED"
            except ConnectionRefusedError:
                return "CONNECTION REFUSED"
                pass

    def getServer(self,key,server_index):
        returnarray = []
        msg = message("GET",key,None,None,None) #nonsense values because message was implemented
                                          #after eventual consistency
        self.sendRequest(msg,server_index, returnarray)
        return returnarray[0]

    def get(self,key):
        if len(self.server_information_dict) != 0:
            server_index = random.randint(0,len(self.server_information_dict)-1)
            return self.getServer(key,server_index)
        else:
            print("Client can't get because the server information dict never got populated.")



    def setServer(self,key,val,server_index):
        returnarray = []
        msg = message("SET",(key,val),None,None,None) #nonsense values because message was implemented
                                          #after eventual consistency
        self.sendRequest(msg,server_index, returnarray)
        return returnarray[0]

    def set(self,key,val):
        if len(self.server_information_dict) != 0:
            server_index = random.randint(0,len(self.server_information_dict)-1)
            return self.setServer(key,val,server_index)
        else:
            print("Client can't set because the server information dict never got populated.")

