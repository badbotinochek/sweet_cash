
import queue


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MessageQueue(queue.Queue, metaclass=Singleton):

    def __init__(self):
        queue.Queue.__init__(self)
