from time import sleep
from threading import Thread, current_thread
from random import randint

def joinall(threads, interval=None):
    pass # TODO: Implement the logic to wait for all threads to complete
         # It must allow reaping threads based on the order of exit.        
        
def fn(count):
    th = current_thread()
    for i in range(count):
        print("In {} counting {}/{}".format(th.name, i, count))
        sleep(0.5)

if __name__ == '__main__':
    threads = []
    for i in range(1, 6):
        t = Thread(target=fn, args=(randint(3, 25),))
        threads.append(t)
        t.start()

    # TODO: Implement this function.
    # First argument should be collection
    # of threads, second argument must
    # be tick interval

    for t in joinall(threads, 0.5):
        print(f"Thread {t.name} exited.")

    print("main complete")
