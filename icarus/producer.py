from .exceptions import TimeoutError
import celery.exceptions
from collector import default_collector


class Producer(object):

    def __init__(self, producer_func, collector=None):
        self.producer_func = producer_func
        self.collector = collector if collector else default_collector
        self.dispatched_items = {}
        self.async_results = []

    def __call__(self, *args, **kwargs):
        return self.__class__(self.producer_func, self.collector)

    def dispatch(self, *args, **kwargs):
        sc = self.producer_func(*args, **kwargs)
        self.async_results = []
        for item in sc:
            self.dispatched_items[item.url] = item
            self.async_results.append(item.handler.delay(item.url, item.content, **item.params))
        return self.async_results

    @property
    def ready(self):
        if not self.dispatched_items:
            raise RuntimeError('Please call run method before check status')

        for ar in self.async_results:
            if not ar.ready():
                return False
        return True

    @property
    def status(self):
        status = {}
        for i in range(len(self.async_results)):
            if self.async_results[i].ready():
                status[self.dispatched_items.keys()[i]] = self.async_results[i].result
            else:
                status[self.dispatched_items.keys()[i]] = None
        return status

    def collect(self, *args, **kwargs):
        timeout = kwargs.get('timeout', 0)
        try:
            return self.collector.collector_func([_.get(timeout=timeout) for _ in self.async_results], *args)
        except celery.exceptions.TimeoutError:
            raise TimeoutError('Failed to get a result in expected time duration {}'.format(timeout))


