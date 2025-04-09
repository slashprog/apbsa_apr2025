from time import sleep, time
from concurrent.futures import ThreadPoolExecutor as Executor



nums = [2, 4, 5, 6, 7, 8, 55, 66, 77, 33, 22, 33, 44, 55, 66]

def square(x):
    sleep(1)
    return x*x

if __name__ == '__main__':

    #result = [ x*x for x in nums ]
    #start = time()
    #result = list(map(square, nums))
    #duration = time() - start
    #print(f"{result=}, {duration=}")

    with Executor(max_workers=6) as workers:
        start = time()
        result = list(workers.map(square, nums))
        duration = time() - start
        print(f"{result=}, {duration=}")
