from random import randint
#from threading import Thread, current_thread as current, Barrier
from multiprocessing import Process as Thread, current_process as current, Barrier
from time import sleep

msg_barrier = Barrier(5)

def random_sleep_and_print(msg):
    thread_name = current().name
    v = randint(5, 30)
    sleep(v)
    print(f"{thread_name}: Woke up!")
    msg.wait()
    print(f"{thread_name}: Continuing!")


if __name__ == '__main__':
    threads = {}
    for i in range(10):
        threads[i] = Thread(target=random_sleep_and_print, args=(msg_barrier,))
        threads[i].start()
    # with Executor(max_workers=10) as workers:
    #      workers.submit(random_sleep_and_print)