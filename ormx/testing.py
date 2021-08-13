from time import time


def timeit(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'{func.__name__!r} executed in {(t2 - t1)}s')
        return result

    return wrap_func


__all__ = [
    'timeit'
]
