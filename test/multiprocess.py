import multiprocessing
import time

def myFunction():
    print("Same process")
    time.sleep(3)

def twoFunc():
    print("two")

if __name__ == "__main__":
    p = multiprocessing.Process(target=myFunction)
    t = multiprocessing.Process(target=twoFunc)
    #p.start() # Запускает процесс
    #p.join() # Ожидает завершение процесса
    t.start()
    t.join()
