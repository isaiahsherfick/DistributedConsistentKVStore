from client_sequential import *
import numpy as np
import numpy.testing as npt


if __name__ == '__main__':
    c = client()
    print("ethan get 5")
    response = c.get(5)
    print(f"ethan received {response}")
    print("ethan set 5 -4")
    response = c.set((5,-4))
    desired = "OK"
    print(f"ethan received {response}")
    gfg = npt.assert_equal(response,desired)
    print("ethan get 5")
    desired = -4
    response = c.get(5)
    print(f"ethan received {response}")
    gfg = npt.assert_equal(response,desired)

    print("ethan finished")
