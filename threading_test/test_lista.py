
import threading
import time

class lista(threading.Thread):

    def __init__(self, l):
        threading.Thread.__init__(self)
        self.l = l

    def run(self):
        print('thread: lista ' + str(l))
        time.sleep(1)
        print('thread dopo sleep: lista ' + str(l))

if __name__ == '__main__':

    l = [(1,'a'),(2,'b'),(3,'c')]
    t = lista(l)
    t.start()

    time.sleep(0.2)
    l[0] = (4,'d')
    print('lista main: ' + str(l))