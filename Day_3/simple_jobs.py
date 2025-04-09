from time import sleep
from multiprocessing import current_process as current

def testfn():
    t = current()
    for i in range(10):
        print(f"{t.name}: counting {i}")
        sleep(1)

def testfn2(v):
    t = current()
    print(f"testfn2 is run as {t.name}")
    sleep(5)
    print(f"testfn2[{t.name}] complete")
    return v*v
