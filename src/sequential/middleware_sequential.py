import time
import pickle
import threading
import socket
import subprocess
import queue
from message import *
from logical_clock import *

class middleware:
    def __init__(self):
        config = open("config",'r')
        configSplit = config.read().split('\n')
        config.close()
        self.num_servers = int(configSplit[2].split('=')[1])
        self.first_server_port = int(configSplit[3].split('=')[1])
        self.top_level_controller_port = int(configSplit[4].split('=')[1])
        self.top_level_controller_host = configSplit[5].split('=')[1]
        self.server_info_dict = {}
        self.jobs = []
        self.clock = logical_clock(-1,0) #only clock with negative id
        self.message_queue = queue.PriorityQueue()
        self.result_table = {}
        self.acknowledgement_table = {}
        currentPort = self.first_server_port
        currentId = 0
        for i in range(self.num_servers):
            self.server_info_dict.update({currentId:currentPort})
            currentId+=1
            currentPort+=1

    def start(self):
        for i in range(self.num_servers):
            print(f"Beginning server process on port {self.server_info_dict.get(i)}")
            self.jobs += [subprocess.Popen(['python3','server_sequential.py',f'{self.server_info_dict.get(i)}',f'{i}'])]
        self.clock.incrementClock()

    def serve(self):
        PORT = self.top_level_controller_port
        HOST = '127.0.0.1'
        t2 = threading.Thread(target=self.processQueue,args=())
        t2.start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            try:
                server.bind((HOST, PORT))
            except OSError:
                print(f"port {PORT} is being blocked.")
                self.terminateJobs()
                exit()

            print("Middleware is listening for messages.")
            server.listen()
            conn, addr = server.accept()
            with conn:
                while True:
                    t = threading.Thread(target=self.enqueueMessage,args=(conn,addr))
                    t.start()
                    server.listen()
                    conn, addr = server.accept()

    def pollResults(self,senderId):
        return self.result_table.get(senderId)

    def allAcknowledgementsReceived(self,server_id):
        if self.acknowledgement_table.get(server_id) == self.num_servers-1:
            return True
        else:
            return False

    def putResult(self,senderId,result):
        self.result_table.update({senderId:result})



    def terminateJobs(self):
        for i in self.jobs:
            i.terminate()
        return

    def handleClocks(self, msg):
        self.clock.adjustClocks(msg.getClock())
        msg.adjustClocks(self.clock)

    def enqueueMessage(self, conn, addr):
        request = pickle.loads(conn.recv(1024))
        if request.getCmd() == "SET":
            server_id = self.serverHash(request.getPayload()[0])
            block_on_broadcast = True
        else:
            block_on_broadcast = False
        self.handleClocks(request)
        self.message_queue.put(request)
        while (self.pollResults(request.getSender()) == None):
            pass
            time.sleep(.1)
        if block_on_broadcast:
            while not self.allAcknowledgementsReceived(server_id):
                time.sleep(.1)
                num = self.acknowledgement_table.get(server_id)
                print(f"{num} Acknowledgements received for server {server_id}.......")
            self.acknowledgement_table.update({server_id:0})

        #print(f"Middleware is now sending {self.pollResults(request.getSender())}")
        conn.send(pickle.dumps(self.pollResults(request.getSender())))
        self.putResult(request.getSender(),None)

    def serverHash(self,key):
        upperBound = len(self.server_info_dict) - 1
        h = key % upperBound
        return h

    def reHash(self,key,previousVal):
        while (h == previousVal):
            upperBound = len(server_info_dict) - 1
            h = random.randint(0,upperBound)
            if h != previousVal:
                return h


    def forwardRequestToServer(self, msg, server_id):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1',self.server_info_dict.get(server_id)))
                s.send(pickle.dumps(msg))
                #print(f"CMD: {msg.getCmd()}")
                if (msg.getCmd() != "SET"):
                    response = pickle.loads(s.recv(1024))
                    return response
                else:
                    pass

            except ConnectionRefusedError:
                newSID = self.reHash(key,server_id)
                self.forwardRequestToServer(msg, newSID)

    #def serveClientResult(self, msg, response):
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #conn = self.getConnection(msg)
            #self.handleClocks(msg)
            #conn.send(pickle.dumps(msg))
            #ack = pickle.loads(s.recv(1024))
            #return ack


    def processQueue(self):
        while True:
            if self.message_queue.empty():
                pass
            else:
                msg = self.message_queue.get()
                #print(f"Dequeueing {msg}")
                if msg.getCmd() == "GET":
                    server_id = self.serverHash(msg.getPayload())
                    response = self.forwardRequestToServer(msg, server_id)
                    #ack = self.serveClientResult(msg,response)
                    self.putResult(msg.getSender(),response)
                elif msg.getCmd() == "SET":
                    server_id = self.serverHash(msg.getPayload()[0])
                    self.forwardRequestToServer(msg, server_id)
                    response = message("OK","OK",server_id,msg.getSender(),self.clock)
                    #ack = self.serveClientResult(msg,response)
                    self.putResult(msg.getSender(),response)
                    pass
                elif msg.getCmd() == "BROADCAST":
                    broadcaster_id = msg.getSender()
                    print(f"server#{broadcaster_id} has started a broadcast.")
                    num_acknowledgements = 0
                    self.acknowledgement_table.update({broadcaster_id:num_acknowledgements})
                    for i in range(self.num_servers):
                        if i == broadcaster_id:
                            pass
                        else:
                            #print(f"broadcasting to server {i}")
                            self.message_queue.put(self.forwardRequestToServer(msg,i))

                elif msg.getCmd() == "ACK":
                    val = self.acknowledgement_table.get(msg.getReceiver())
                    val+=1
                    self.acknowledgement_table.update({msg.getReceiver():val})
                    if (self.allAcknowledgementsReceived(server_id)):
                        print("Total order broadcast successful, preparing to serve set request")
                else:
                    pass
        return






if __name__ == '__main__':
    m = middleware()
    m.start()
    try:
        m.serve()
    except KeyboardInterrupt:
        m.terminateJobs()
        exit()
