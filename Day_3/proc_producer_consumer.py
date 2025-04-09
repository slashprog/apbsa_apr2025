from multiprocessing import Process, Queue
from time import sleep

def generate_values(q):
    from random import randint, random
    while True:
        v = randint(1, 100)
        q.put(v)
        print("Producer: added: ", v)
        sleep(random())

def get_values(q):
    from random import random
    while True:
        v = q.get()
        print("Consumer: consumed: ", v)
        sleep(random())


if __name__ == '__main__':
    q = Queue(5)
    producer = Process(target=generate_values, args=(q,))
    consumer = Process(target=get_values, args=(q,))

    producer.start()
    consumer.start()

    sleep(10)
    producer.terminate()
    consumer.terminate()
