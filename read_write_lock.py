from threading import Lock, Condition
INIT_MODE = 0
READ_MODE = 1
WRITE_MODE = 2

## todo support timeout
## todo how to avoid write starvation
class ReadWriteLock():
    def __init__(self):
        self.mode = INIT_MODE
        self.mutex = Lock()
        self.readers = 0
        self.read_cond = Condition()
        self.write_cond = Condition()

    def acquire_read(self):
        try:
            self.mutex.acquire()
            if self.mode == READ_MODE:
                self.readers += 1
            elif self.mode == INIT_MODE:
                self.mode = READ_MODE
                self.readers += 1
            elif self.mode == WRITE_MODE:
                with self.read_cond:
                    self.read_cond.wait()
            else:
                raise ValueError("invalid mode")

        finally:
            self.mutex.release()

    def release_read(self):
        try:
            self.mutex.acquire()

            if self.mode == READ_MODE:
                self.readers -= 1
                if self.readers <= 0:
                    self.mode = INIT_MODE
                    with self.write_cond:
                        self.write_cond.notify()

            elif self.mode == INIT_MODE or self.mode == WRITE_MODE:
                pass
        finally:
            self.mutex.release()


    def acquire_write(self):
        self.mutex.acquire()

        if self.mode == READ_MODE or  self.mode == WRITE_MODE:
            self.write_cond.wait()
        elif self.mode == INIT_MODE:
            self.mode = WRITE_MODE

        self.mutex.release()

    def release_write(self):
        self.mutex.acquire()

        if self.mode == WRITE_MODE:
            self.mode = INIT_MODE
            with self.write_cond:
                self.write_cond.notify()
            with self.read_cond:
                self.read_cond.notify_all()
        elif self.mode == READ_MODE or self.mode == INIT_MODE:
            raise ValueError("invalid mode")

        self.mutex.release()