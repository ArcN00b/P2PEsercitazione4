
import threading
import time
import random

## questa classe lancia costantemente 10 thread per fare un lavoro
class Test(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        max_t = 10
        cont_t = 2
        semaphore = threading.BoundedSemaphore(cont_t)
        threads = []
        num_t = 0

        for i in range(0, max_t):

            semaphore.acquire()
            t = Parallel(semaphore, i)
            threads += [t]
            t.start()
            print('numero thread in lista: ' + str(len(threads)))
        for x in threads:
            x.join()

        print('finish test thread')

class Parallel(threading.Thread):

    def __init__(self, semaphore, i):
        threading.Thread.__init__(self)
        self.semaphore = semaphore
        self.i = i

    def run(self):
        r = random.random()
        print('execute thread parallel: ' + str(self.i) + ', sleeping for: ' + str(r))
        time.sleep(r)
        print('finish thread parallel: ' + str(self.i))
        self.semaphore.release()

if __name__ == '__main__':

    big = Test()
    big.start()
    print('finish main thread')

    big.join()

