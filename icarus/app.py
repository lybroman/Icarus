from celery import Celery
from functools import wraps
from splitter import Splitter
from integrator import Integrator


class Icarus(Celery):
    def __init__(self, name, backend, broker):
        super(Icarus, self).__init__(name, backend=backend, broker=broker)
        self._splitters = []

    def splitter(self, *args, **kwargs):

        if not callable(args[0]):
            raise TypeError("Splitter must be a callable object")
        splitter_instance = Splitter(args[0])
        self._splitters.append(splitter_instance)
        return splitter_instance

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

    def integrator(self, *args, **opt):

        if args[0] not in self._splitters:
            raise TypeError("Splitter %s is not registered".format(args[0]))

        if not callable(args[0]):
            raise TypeError("Splitter must be a callable object")

        def _wrapper(integrator_func):
            if not callable(integrator_func):
                raise TypeError("Integrator must be a callable object")

            args[0].integrator = Integrator(integrator_func)
            return args[0].integrator

        return _wrapper

    @property
    def default_handler(self):
        @self.handler
        # only a function signature
        def func_handler(url, *args):
            pass
        return func_handler
