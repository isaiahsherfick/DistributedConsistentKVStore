from client_sequential import *
import numpy as np
import numpy.testing as npt


if __name__ == '__main__':
    c = client()
    print("rupert set 20 -4")
    response = c.set((20,-4))
    desired = "OK"
    print(f"rupert received {response}")
    gfg = npt.assert_equal(response,desired)
    print("rupert get 20")
    desired = -4
    response = c.get(20)
    print(f"rupert received {response}")
    gfg = npt.assert_equal(response,desired)

    print("rupert finished")
