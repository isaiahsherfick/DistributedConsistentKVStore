import time
import pickle
import socket
import subprocess
from message import *



if __name__ == '__main__':
    #handle config variables on startup
    configFile = open("config", "r")
    configSplit = configFile.read().split('\n')[0:-1]
    configFile.close()
    consistency = configSplit[0].split('=')[1]
    if (consistency not in ['sequential','eventual','linearizability']):
        print("Error in config file; eventual consistency selected by default.")
        consistency = 'eventual'
    num_clients = int(configSplit[1].split('=')[1])
    num_servers = int(configSplit[2].split('=')[1])
    first_server_port= int(configSplit[3].split('=')[1])
    top_level_controller_port = int(configSplit[4].split('=')[1])
    top_level_controller_host = configSplit[5].split('=')[1]

    #will map unique int ids to port# for each server
    server_info_dict = {}

    #populate server_info_dict
    currentPort = first_server_port
    currentServerID = 0
    for i in range(num_servers):
        server_info_dict.update({currentServerID:currentPort })
        currentServerID = currentServerID + 1
        currentPort = currentPort + 1

    server_jobs = []
    middleware_jobs = []


    for i in server_info_dict:
        print(f"Beginning server process on port {server_info_dict.get(i)}")
        if (consistency == 'eventual'):
            server_jobs += [subprocess.Popen(['python3','server_eventual.py','127.0.0.1',f'{server_info_dict.get(i)}',f'{consistency}'])]
        elif (consistency == 'sequential'):
            server_jobs += [subprocess.Popen(['python3','server_sequential.py','127.0.0.1',f'{server_info_dict.get(i)}',f'{consistency}'])]
            #so this only happens once
            if (i == 0):
                middleware_jobs += [subprocess.Popen(['python3','middleware_sequential.py','127.0.0.1',f'{server_info_dict.get(i)}',f'{consistency}'])]
        elif (consistency == 'linearizable'):
            server_jobs += [subprocess.Popen(['python3','server_linearizable.py','127.0.0.1',f'{server_info_dict.get(i)}',f'{consistency}'])]
            #so this only happens once
            if (i == 0):
                middleware_jobs += [subprocess.Popen(['python3','middleware_linearizable.py','127.0.0.1',f'{server_info_dict.get(i)}',f'{consistency}'])]
        else:
            print("Consistency error")
            exit()

    print("All processes spawned.")

    #start a server that will listen for new clients and serve the pickle
    #with server info to that new client



    PORT = top_level_controller_port
    HOST = '127.0.0.1'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        try:
            server.bind((HOST, PORT))
        except OSError:
            print(f"port {PORT} is being blocked.")
            exit()
        print("Listening for connections from new clients.")
        server.listen()


        conn, addr = server.accept()
        with conn:
            while True:
                conn.send(pickle.dumps(server_info_dict))

                server.listen()
                try:
                    conn, addr = server.accept()
                except KeyboardInterrupt:
                    print("\nExiting...")
                    for i in server_jobs:
                        i.terminate()

                    exit()
