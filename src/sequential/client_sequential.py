import socket
import os
import random
import sys
import time
import pickle
from message import *
from logical_clock import *


class client:
    def __init__(self):
        config = open("config",'r')
        configSplit = config.read().split('\n')
        config.close()
        self.id = os.getpid()
        self.clock = logical_clock(self.id,0)
        self.middleware_port = int(configSplit[4].split('=')[1])

    def getId(self):
        return self.id

    def getClock(self):
        return self.clock

    def get(self, key):
        #-1 in sender_pid == middleware will autoassign
        msg = message("GET", key, self.getId(), -1, self.clock)
        return self.sendRequest(msg)

    def set(self, kvTuple):
        #-1 in sender_pid == middleware will autoassign
        msg = message("SET", kvTuple, self.getId(), -1, self.clock)
        return self.sendRequest(msg)
    def handleClocks(self,otherClock):
        self.clock.adjustClocks(otherClock)

    def sendRequest(self,msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1',self.middleware_port))
                s.send(pickle.dumps(msg))
                response = s.recv(1024)
                try:
                    data = pickle.loads(response)
                    try:
                        other_clock = data.getClock()
                        self.handleClocks(other_clock)
                        return data.getPayload()
                    except AttributeError:
                        pass
                        return data
                except EOFError:
                    return "CONNECTION INTERRUPTED"
            except ConnectionRefusedError:
                return "CONNECTION REFUSED"
                pass

if __name__ == '__main__':
    c = client()
    c.get(random.randint(0,100))
    time.sleep(random.randint(1,4))
