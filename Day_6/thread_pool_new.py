from threading import Thread, Event
from queue import Queue

#from multiprocessing import Process as Thread, Event, Queue


class ThreadPool:
    def __init__(self, max_workers):
        self.queue = Queue(max_workers)
        self.workers = []
        self.quit = False

    def start(self):
        for i in range(self.queue.maxsize):
            w = Thread(target=self.__wait_on_queue, name=f"worker-{i+1}")
            self.workers.append(w)
            w.start()

    def __wait_on_queue(self):
        while not self.quit:
            result = self.queue.get()
            
            if result is None:
                break

            if result.state == "QUEUED":
                result.execute()

    def shutdown(self):
        self.quit = True
        while not self.queue.full():
            self.queue.put(None)
        
        for w in self.workers:
            w.join()

    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, et, ev, tb):
        self.shutdown()

    def submit(self, fn, args=(), kwargs={}):
        result = Result(fn, args, kwargs)
        result.state = "QUEUED"
        self.queue.put(result)
        return result

class Result:
    def __init__(self, fn, args, kwargs): 
        self.fn, self.fn_args, self.fn_kwargs = fn, args, kwargs
        self.__state = "INITIALIZED" 
        self.result_value = None
        self.done = Event()

    def execute(self):
        if self.state != "CANCELLED":
            self.state = "RUNNING"
            self.result_value = self.fn(*self.fn_args, **self.fn_kwargs)
            self.state = "FINISHED"
            self.done.set()

    @property
    def result(self):
        self.done.wait()
        return self.result_value
        
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, s):
        if s in ("QUEUED", "RUNNING", "FINISHED", "CANCELLED"):
            self.__state = s
        else:
            raise ValueError(f"Result state can either be - QUEUED, RUNNING, CANCELLED or FINISHED, not {s}")

    def cancel(self):
        if self.state == "QUEUED":
            self.state = "CANCELLED"
            return True
        else:
            return False
    
