from threading import Thread, Event, current_thread
from queue import Queue

class Job:
    def __init__(self, fn, args=(), kwargs={}):
        self.return_value = Queue(1)
        self.ready = False
        self.status = "queued"
        self.fn, self.args, self.kwargs = fn, args, kwargs

    def run(self):
        self.status = "inflight"
        ret = self.fn(*self.args, **self.kwargs)
        self.status = "done"
        self.return_value.put(ret)
        self.ready = True

    def result(self):
        return self.return_value.get()

class ThreadPool:
    def __init__(self, max_workers):
        self.queue = Queue(max_workers)
        self.workers = []
        self.quit = Event()
        for i in range(max_workers):
            t = Thread(target=self.__wait_on_queue, name=f"ThreadPool-Worker-{i+1}")
            self.workers.append(t)

    def __wait_on_queue(self):
        while not self.quit.is_set():
            job = self.queue.get()
            if job is None:
                continue
            job.run()

    def start(self):
        for t in self.workers:
            t.start()
        self.quit.clear()

    def stop(self):
        self.quit.set()
        for _ in self.workers:
            self.queue.put(None)

    def __enter__(self):
        self.start()

    def __exit__(self, et, ev, tb):
        self.stop()

    def submit(self, fn, args=(), kwargs={}):
        job = Job(fn, args, kwargs)
        self.queue.put(job)
        return job
