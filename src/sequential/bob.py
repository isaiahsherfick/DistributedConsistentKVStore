from client_sequential import *
import numpy as np
import numpy.testing as npt


if __name__ == '__main__':
    c = client()
    desired = "OK"
    print("bob set 20 654")
    response = c.set((20,654))
    gfg = npt.assert_equal(response,desired)
    desired = 654
    print("bob get 20")
    response = c.get(20)
    print(f"bob received {response}")
    gfg = npt.assert_equal(response,desired)
    print("bob finished")
