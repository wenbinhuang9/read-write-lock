# read-write-lock
A simple implementation of read write lock. 

1. using mutual lock to protect critical section
2. using condition variable to achieve wait/notify synchronization control

# Code

```
lock = ReadWriteLock()

lock.acquire_read()
lock.release_read()

lock.acquire_write()
lock.release_write()
```

