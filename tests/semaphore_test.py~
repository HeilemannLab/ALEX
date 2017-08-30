from multiprocessing import Semaphore, Process, freeze_support
import time


def Worker(N, semaphore):
    print("Worker %i started." % N)
    time.sleep(N)
    semaphore.acquire()
    print("Worker %i exits." % N)


if __name__=='__main__':
    freeze_support()
    semaphore = Semaphore(3)
    processes = []

    start = time.time()

    for i in range(3):
        p = Process(target=Worker, args=(i, semaphore))
        p.start()
        processes.append(p)

    while semaphore.get_value() > 0:
        pass
    end = time.time()
    while not semaphore.get_value() == 3:
        semaphore.release()
    print("Semaphore counter reached 0 after %f seconds" % (end - start))
