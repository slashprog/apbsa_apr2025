def add(x, y):
    print(f"add method invoked: x={x}, y={y}")
    return x+y

def add_slow(x, y):
    print(f"add_slow function called: {x=}, {y=}")
    from time import sleep
    sleep(10)
    print(f"add_slow function complete. Returning {x+y}")
    return x+y

def add_slow_busy(x, y):
    print(f"add_slow_busy function called: {x=}, {y=}")
    for _ in range(10_000_000): pass
    print(f"add_slow_busy function complete. Returning {x+y}")
    return x+y

