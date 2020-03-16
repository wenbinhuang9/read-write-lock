import unittest
from read_write_lock import ReadWriteLock
from threading import Thread
class TinyDB():
    def __init__(self):
        self.count = 0
        self.lock = ReadWriteLock()
    def get(self):
        self.lock.r_acquire()
        count = self.count
        self.lock.r_release()
        return count

    def increase(self):
        self.lock.w_acquire()
        self.count += 1
        self.lock.w_release()
        return self.count

class MyTestCase(unittest.TestCase):
    def test_writer(self):
        db = TinyDB()
        def write(db, thread_id):
            count = db.increase()
            print("count={0}|thread_id={1}".format(count, thread_id))

        threads = []

        for i in range(10):
            t = Thread(target=write, args=(db, i,))
            threads.append(t)
        for t in threads:
            t.start()


    def test_read(self):
        db = TinyDB()

        def read(db, thread_id):
            ans = db.get()
            print("count = {0} |thread_id = {1}".format(ans, thread_id))
        threads = []

        for i in range(10):
            t = Thread(target=read, args=(db, i,))
            threads.append(t)

        for t in threads:
            t.start()


if __name__ == '__main__':
    unittest.main()
