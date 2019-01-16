from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
import tornado.gen

q = Queue(maxsize=2)

@tornado.gen.coroutine
def consumer():
    while True:
        item = yield q.get()
        try:
            print('Doing work on %s' % item)
            yield tornado.gen.sleep(0.01)
        finally:
            q.task_done()

@tornado.gen.coroutine
def producer():
    for item in range(5):
        yield q.put(item)
        print('Put %s' % item)

@tornado.gen.coroutine
def main():
    # Start consumer without waiting (since it never finishes).
    ioloop = IOLoop.current()
    ioloop.spawn_callback(consumer)
    yield producer()
    yield q.join()
    print('Done')

IOLoop.current().run_sync(main)