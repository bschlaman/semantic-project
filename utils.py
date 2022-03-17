import time

# used to time individual functions
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(f" - time: {(time.perf_counter() - start):.3f}")
        return res
    return wrapper
