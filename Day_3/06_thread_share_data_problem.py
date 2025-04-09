from threading import Thread, Lock
from time import sleep
from random import random

SIZE = 100

nums = list(range(SIZE))
nums_lock = Lock()

def pick_elements(dataset, howmany, result):
    for _ in range(howmany):
        with nums_lock:
            value = dataset[0]
            result.append(value)
            sleep(random() / 10)
            del dataset[0]
            
        #result.append(dataset.pop())

def pick_elements_legacy_buggy(dataset, howmany, result):
    for _ in range(howmany):
        
        nums_lock.acquire()
        
        value = dataset[0]
        result.append(value)
        sleep(random() / 10)
        del dataset[0]

        nums_lock.release()

def pick_elements_legacy_better(dataset, howmany, result):
    for _ in range(howmany):
        
        try:
            nums_lock.acquire()
        
            value = dataset[0]
            result.append(value)
            sleep(random() / 10)
            del dataset[0]

        finally:
            nums_lock.release()



if __name__ == '__main__':
    result1 = []
    result2 = []

    backup = nums.copy()

    t1 = Thread(target=pick_elements, args=(nums, SIZE//2, result1))
    t2 = Thread(target=pick_elements, args=(nums, SIZE//2, result2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("nums = ", nums)
    print(set(result1) & set(result2))
    print(set(backup) - (set(result1) | set(result2)))
    #print(f"{result1=}, {result2=}")
