import time
import threading
from client_sequential import *
import subprocess
import numpy as np
import numpy.testing as npt

#these functions will be a series of write/read orderings that
#will be executed concurrently to check for consistency




def p0():
    c1 = client()
    desired = "OK"
    print("p0 set 12 100")
    response = c1.set((12,100))
    gfg = npt.assert_equal(response, desired)
    print("p0 finished")





def p1():
    c1 = client()
    desired = "OK"
    actual = c1.get(12)
    gfg = npt.assert_equal(actual,desired)
    print("p1 set 12 abc")
    c1.set((12,'abc'))
    desired2 = 'abc'
    actual2 = c1.get(12)
    gfg = npt.assert_equal(actual2,desired2)
    print("p1 finished")


def p2():
    c1 = client()
    desired = "OK"
    print("p2 set 20 0")
    actual = c1.set((20, 0))
    gfg = npt.assert_equal(actual,desired)
    desired = 0
    actual = c1.get(20)
    gfg = npt.assert_equal(actual,desired)
    print("p2 finished")



def p3():
    c1 = client()
    desired = "OK"
    print("p2 set 20 1234")
    actual = c1.set((20, 1234))
    gfg = npt.assert_equal(actual,desired)
    desired = 1234
    actual = c1.get(20)
    gfg = npt.assert_equal(actual,desired)
    print("p3 finished")




def test1():
    t0 = threading.Thread(target=p0)
    t1 = threading.Thread(target=p1)
    t2 = threading.Thread(target=p2)
    t3 = threading.Thread(target=p3)
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t0.join()
    t1.join()
    t2.join()
    t3.join()

if __name__ == '__main__':
    jobs = []
    jobs += [subprocess.Popen(["python3","middleware_sequential.py"])]
    time.sleep(5)
    test1()
    time.sleep(20)

