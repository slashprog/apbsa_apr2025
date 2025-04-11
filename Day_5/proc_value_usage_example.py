from concurrent.futures import ProcessPoolExecutor as Executor
from multiprocessing import Process, Value, current_process as current

stats = {
    "usage_count": Value("i", 0),
    "connections": Value("i", 0)
}


from time import sleep

def handle_client(c, u):
    from random import random, randint
    from time import sleep

    c.value += 1

    while True:
        sleep(randint(1, 10))
        u.value += 1
 

def show_stats(c, u):
    from time import sleep
    while True:
        sleep(5)
        print(f"Usage: {u.value}, Connections: {c.value}")



if __name__ == '__main__':

    Process(target=show_stats, args=(stats["connections"], stats["usage_count"])).start()

    with Executor(max_workers=6) as workers:
        for i in range(6):
            workers.submit(handle_client, stats["connections"], stats["usage_count"])
