from .exceptions import TimeoutError
import celery.exceptions


class Splitter(object):

    def __init__(self, splitter_func, integrator=None):
        self.splitter_func = splitter_func
        self.integrator = integrator
        self.segments = {}
        self.async_results = []

    def __call__(self, *args, **kwargs):
        return Splitter(self.splitter_func, self.integrator)

    def dispatch(self, *args, **kwargs):
        segments = self.splitter_func(*args, **kwargs)
        self.segments = {}
        self.async_results = []
        for segment in segments:
            self.segments[segment[0]] = segment[1:]
            self.async_results.append(segment[0].delay(*(segment[1:])))
        return self.async_results

    @property
    def ready(self):
        if len(self.segments) == 0:
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
                status[self.segments.keys()[i]] = self.async_results[i].result
            else:
                status[self.segments.keys()[i]] = None
        return status

    def integrate(self, *args, **kwargs):
        timeout = kwargs.get('timeout', 0)
        try:
            return self.integrator.integrator_func([_.get(timeout=timeout) for _ in self.async_results], *args)
        except celery.exceptions.TimeoutError:
            raise TimeoutError('Failed to get a result in expected time duration {}'.format(timeout))


