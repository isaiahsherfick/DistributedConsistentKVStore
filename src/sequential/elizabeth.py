from client_sequential import *
import numpy as np
import numpy.testing as npt


if __name__ == '__main__':
    c = client()
    print("elizabeth set 500 9")
    response = c.set((500,9))
    desired = "OK"
    print(f"elizabeth received {response}")
    gfg = npt.assert_equal(response,desired)
    print("elizabeth get 500")
    desired = 9
    response = c.get(500)
    print(f"elizabeth received {response}")
    gfg = npt.assert_equal(response,desired)

    print("elizabeth finished")
