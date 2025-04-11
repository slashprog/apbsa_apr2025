"""
Implement 'thread_pool' module hosting 'ThreadPool'
class that allows us to create a pool of worker threads
waiting on a job-queue for any jobs (functions) to be
submitted.

Implement the ThreadPool class such that the code within
the '__main__' namespace works.

"""
from thread_pool import ThreadPool
from threading import current_thread as current

if __name__ == '__main__':

    def foo(x, y):
        print(f"foo[{current()}] called with {x=}, {y=}")
        return x + y

    def bar(x, y):
        print(f"bar[{current()}] called with {x=}, {y=}")
        return x * y

    def test(x):
        print(f"test[{current()}] called with {x=}")
        return x ** x

    def square(x):
        print(f"square[{current()}] called with {x=}")
        from time import sleep
        sleep(0.5)
        return x*x

    with ThreadPool(max_workers=10) as pool:
        foo_result = pool.submit(fn=foo, args=(10, 20))
        bar_result = pool.submit(fn=bar, args=("Hello", 10))
        test_result = pool.submit(fn=test, args=(100,))
        square_result = pool.submit(fn=square, args=(4,))
        
        print("Jobs submitted, waiting for result")

    print(foo_result.result, bar_result.result, test_result.result)

