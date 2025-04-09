
class WorkerPool:
    def __init__(self, max_workers):
        pass # TODO

    def start(self):
        pass # TODO

    def shutdown(self):
        pass # TODO

    def __enter__(self):
        self.start()
    
    def __exit__(self, et, ev, tb):
        self.shutdown()

    def submit(self, fn, args=(), kwargs={}):
        pass # TODO

class Result:
    def __init__(self, fn, args, kwargs): 
        pass # TODO

    def execute(self):
        pass # TODO

    @property
    def result(self):
        pass # TODO
           
    @property
    def state(self):
        pass # TODO

    @state.setter
    def state(self, s):
        pass # TODO

    def cancel(self):
        pass # TODO

