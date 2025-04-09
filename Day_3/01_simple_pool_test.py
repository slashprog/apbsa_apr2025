from multiprocessing import Pool, current_process as current
from time import sleep

def testfn():
    t = current()
    for i in range(10):
        print(f"{t.name}: counting {i}")
        sleep(1)
    
if __name__ == '__main__':
    p = Pool(10)
    r1 = p.apply_async(testfn)
    r2 = p.apply_async(testfn)
    print(r1, r2)
    
    sleep(10)
    print("Tasks completed...")
