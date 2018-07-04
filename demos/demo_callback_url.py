from icarus import Icarus, Suitcase
import time

nirvana = Icarus('tasks', backend='db+postgresql://postgres:postgres@localhost:5432/postgres', broker='pyamqp://guest@localhost//')


@nirvana.producer
def produce(entity):
	sc = Suitcase()

	for item in entity:
		if item == 'foo':
			sc.package_item(handler=nirvana.default_handler, url='foo-api', content='say foo!', callback_url="http://httpbin.org/anything")
		elif item == 'bar':
			sc.package_item(handler=nirvana.default_handler, url='bar-api', content='say bar!', callback_url="http://httpbin.org/anything")

	return sc


"""
# you could define your own collector and 
# register it with the producer
@nirvana.collector(produce)
def collect(results):
	return [_ for _ in results]
"""


x = produce()

x.dispatch(['foo', 'bar'])

t = time.time()
while True:
	if x.ready:
		print 'All results ready!'
		break
	else:
		time.sleep(1)
		print 'Wait all results ready...'

print x.collect(timeout=1)

print 'Time used: ', time.time() - t

