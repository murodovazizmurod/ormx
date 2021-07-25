import time


def timeit(method, db):
    def timed(*args, **kw):
        if db.config['testing']:
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            print('\n\n____________________\n%r  %2.2f ms\n____________________' % \
                  (method.__name__, (te - ts) * 1000))
            return result
        return method(*args, **kw)

    return timed


def timeit(db):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if db.config['testing']:
                ts = time.time()
                result = function(*args, **kwargs)
                te = time.time()
                print('\n\n____________________\n%r  %2.2f ms\n____________________' % \
                      (function.__name__, (te - ts) * 1000))
            else:
                result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator
