__author__ = 'kelvin'

from concurrent.futures import ThreadPoolExecutor
from cafe.core.decorators import SingletonClass

class _CThreadPool(ThreadPoolExecutor):
    """
    subclass from concurrent.futures.ThreadPoolExecutor
    """
    manager = None
    def __init__(self, manager, name, max_workers=10):
        self.manager = manager
        self.name = name
        ThreadPoolExecutor.__init__(self, max_workers)
        self.manager.pool[name] = self

    def run(self, fn, *args, **kwargs):
        """
        function executor
        :param fn: function object
        """
        self.submit(fn, *args, **kwargs)

    def join(self, wait=True):
        ThreadPoolExecutor.shutdown(self, wait)
        if not self.manager is None:
            self.manager.remove(self.name)


@SingletonClass
class NamedThreadPoolManager(object):
    """
    Collection of ThreadPoolExecutor objects
    """
    pool = {}

    def get(self, name):
        """
        get thread pool object by name
        :param name:
        :return: thread pool object
        """
        if name in self.pool:
            return self.pool[name]
        else:
            t = _CThreadPool(self, name, max_workers=10)
            return t

    def exists(self, name):
        """
        test if "name" already exist
        :param name: name of thread pool
        :return: True/False
        """
        return name in self.pool

    def set_pool_worker_max(self, name, max):
        """
        set max number of function can run in parallel
        :param name: name of thread pool
        :param max: max. number of functions can be run in parallel
        :return:
        """
        if not name in self.pool:
            raise RuntimeError()
        self.pool[name]._max_workers = max

    def remove(self, name):
        """
        remove thread pool of <name>
        :param name:
        :return:
        """
        if self.exists(name):
            self.pool.pop(name)

def get_thread_pool(name="default"):
    """
    get thread pool object by name
    :param name:
    :return: threadpool object
    """
    return NamedThreadPoolManager().get(name)

def wait_thread_pool(name):
    """
    wait all functions in thread pool of <name> complete
    :param name:
    :return:
    """
    n = NamedThreadPoolManager()
    if not n.exists(name):
        return
    t = n.get(name)
    t.shutdown(wait=True)
    n.remove(name)

if __name__ == "__main__":
    import threading
    import time
    def t(a):
        for i in range(10):
            print ("%s: %s" % (threading.currentThread().name, str(a)) )
            time.sleep(1)
    x = get_thread_pool(name="hello")
    x.run(t, 6)
    x.run(t, 8)
    x.join()
    #wait_thread_pool("hello")
    x = get_thread_pool(name="hello")
    x.run(t, 9)