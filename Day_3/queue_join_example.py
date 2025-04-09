#from threading import Thread as Task, current_thread as current
#from queue import Queue

from multiprocessing import Process as Task, current_process as current, JoinableQueue as Queue
from time import sleep

q = Queue(2)

def producer():
    q.put("Test data")
    print(f"producer[{current()}]: added a string to queue.")
    q.join()
    print(f"producer[{current()}]: got acknowledgement from consumer.")

def consumer():
    sleep(5)
    v = q.get()
    print(f"consumer[{current()}]: fetched an element from queue: v = {v}")
    sleep(3)
    q.task_done()
    print(f"consumer[{current()}]: sent acknowledgement.")

if __name__ == '__main__':
    t1 = Task(target=producer)
    t2 = Task(target=consumer)
    t1.start()
    t2.start()

