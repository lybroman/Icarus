from icarus import Icarus
import time

nirvana = Icarus('tasks', backend='db+postgresql://postgres:postgres@localhost:5432/postgres', broker='pyamqp://guest@localhost//')


@nirvana.splitter
def enter(entity):
    items = list()
    for item in entity:
        if item == 'foo':
            items.append((nirvana.default_handler, 'foo-api', 'say foo!'))
        elif item == 'bar':
            items.append((nirvana.default_handler, 'bar-api', 'say bar!'))

    return items


@nirvana.integrator(enter)
def leave(ls):
    return [_ for _ in ls]


e = enter()

e.dispatch(['foo', 'bar'])

t = time.time()
while True:
    if e.ready:
        print 'All results ready!'
        break
    else:
        time.sleep(1)
        print 'Wait all results ready...'

print e.integrate(timeout=1)

print 'Time used: ', time.time() - t

