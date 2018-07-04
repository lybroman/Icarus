from celery import Celery
from functools import wraps
from producer import Producer
from collector import Collector


class Icarus(Celery):
    def __init__(self, name, backend, broker):
        super(Icarus, self).__init__(name, backend=backend, broker=broker)
        self._producers = []

    def producer(self, *args, **kwargs):

        if not callable(args[0]):
            raise TypeError("Producer must be a callable object")
        producer_instance = Producer(args[0])
        self._producers.append(producer_instance)
        return producer_instance

    def handler(self, *args, **opt):

        if not callable(args[0]):
            raise TypeError("Handler must be a callable object")

        def _wrapper(handler_func):
            @self.task(**opt)
            @wraps(handler_func)
            def __wrapper(*args, **kwargs):
                return handler_func(*args, **kwargs)
            return __wrapper
        return _wrapper(args[0])

    def collector(self, *args, **opt):

        if args[0] not in self._producers:
            raise TypeError("Producer %s is not registered".format(args[0]))

        if not callable(args[0]):
            raise TypeError("Producer must be a callable object")

        def _wrapper(collector_func):
            if not callable(collector_func):
                raise TypeError("Integrator must be a callable object")

            args[0].collector = Collector(collector_func)
            return args[0].collector

        return _wrapper

    @property
    def default_handler(self):
        @self.handler
        # only a function signature
        def func_handler(url, content, **kwargs):
            pass
        return func_handler
