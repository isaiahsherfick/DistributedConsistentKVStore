from client_sequential import *
import numpy as np
import numpy.testing as npt


if __name__ == '__main__':
    c = client()
    desired = "OK"
    print("alice set 12 100")
    response = c.set((12,100))
    print(f"alice received {response}")
    gfg = npt.assert_equal(response,desired)
    print("alice finished")
