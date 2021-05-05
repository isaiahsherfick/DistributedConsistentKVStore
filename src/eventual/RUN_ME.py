import time
import threading
from client_eventual import *
import subprocess
import numpy as np
import numpy.testing as npt
import timer

#these functions will be a series of write/read orderings that
#will be executed concurrently to check for consistency



def spawnController():
    jobs = []
    jobs += [subprocess.Popen(["python3","top_level_controller.py"])]

def p1():
    c1 = client()
    desired = None
    actual = c1.get(12)
    gfg = npt.assert_equal(actual,desired)
    time.sleep(1)
    desired = "OK"
    actual = c1.set(12,'abc')
    gfg = npt.assert_equal(actual,desired)
    desired2 = 'abc'
                            #putting a time.sleep(1) here makes
    #<---------------       #eventual consistency pass this every time
    time.sleep(3)
                            #without, however, it fails most of the time
    actual2 = c1.get(12)
    gfg = npt.assert_equal(actual2,desired2)


def p2():
    c1 = client()
    desired = "OK"
    actual = c1.set(20, [1,2,3])
    gfg = npt.assert_equal(actual,desired)
    desired = [1,2,3]
    time.sleep(3) #<---- #similar to p1, if you put a time.sleep(2) here,
                         #the system using eventual consistency will pass
                         #not without it though unless it happens to ping the same
                         #server twice (unlikely)
    actual = c1.get(20)
    gfg = npt.assert_equal(actual,desired)



def p3():
    c1 = client()
    desired = "OK"
    actual = c1.set(20, 1234)
    gfg = npt.assert_equal(actual,desired)
    time.sleep(3)
    desired = 1234
    actual = c1.get(20)
    pass




def test1():
    t1 = threading.Thread(target=p1)
    t2 = threading.Thread(target=p2)
    t3 = threading.Thread(target=p3)
    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()
def test2():
    t1 = threading.Thread(target=p1)
    t2 = threading.Thread(target=p2)
    t3 = threading.Thread(target=p3)
    t3.start()
    t3.join()
    t2.start()
    t2.join()
    t1.start()
    t1.join()

if __name__ == '__main__':
    configFile = open("config","w")
    configFile.write("consistency=eventual\nnum_clients=2\nnum_servers=20\nfirst_server_port=65432\ntop_level_controller_port=65431\ntop_level_controller_host=127.0.0.1\n")
    configFile.close()
    spawnController()
    time.sleep(8)
    test1()
    print("All tests passed if there are no assertion errors above this print!")
