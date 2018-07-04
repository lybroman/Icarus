class Collector(object):
    def __init__(self, collector_func):
        self.collector_func = collector_func


default_collector = Collector(lambda x: [_ for _ in x])

if __name__ == '__main__':
    assert default_collector.collector_func([1, 2, 3]) == [1, 2, 3]

