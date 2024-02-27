
def profile(func):
    def wrap(*args, **kwargs):
        import time, logging
        started_at = time.time()
        result = func(*args, **kwargs)
        logging.info(time.time() - started_at)
        return result

    return wrap



def profile2(func):
    def wrapper(*args, **kwargs):
        import cProfile, sys
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.print_stats()
        return retval

    return wrapper

