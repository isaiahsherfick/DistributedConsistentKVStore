import time
import subprocess

if __name__ == "__main__":
    jobs = []
    jobs += [subprocess.Popen(["python3","middleware_sequential.py"])]
    time.sleep(5)
    jobs += [subprocess.Popen(["python3","alice.py"])]
    time.sleep(.5)
    jobs += [subprocess.Popen(["python3","bob.py"])]
    time.sleep(.5)
    jobs += [subprocess.Popen(["python3","rupert.py"])]
    time.sleep(.5)
    jobs += [subprocess.Popen(["python3","ethan.py"])]
    time.sleep(.5)
    jobs += [subprocess.Popen(["python3","elizabeth.py"])]
    time.sleep(5)
    print("Testing done")
