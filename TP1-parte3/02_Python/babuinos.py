import sys
import threading
import time
import random


MAX_BABUINOS = 5


def babuinos(N, M):
    semaforo = threading.Semaphore(MAX_BABUINOS)
    sem_izq = threading.Semaphore(MAX_BABUINOS)
    sem_der = threading.Semaphore(MAX_BABUINOS)
    babuinos = []

    for _ in range(N):
        babuinos.append(threading.Thread(target=cruzar_soga, args=(
            semaforo, sem_izq, sem_der, True)))

    for _ in range(M):
        babuinos.append(threading.Thread(target=cruzar_soga, args=(
            semaforo, sem_izq, sem_der, False)))

    random.shuffle(babuinos)
    for babuino in babuinos:
        babuino.start()
        time.sleep(random.randint(1, 2))


def cruzar_soga(semaforo, sem_izq, sem_der,  es_izquierda):
    semaforo.acquire()
    if es_izquierda and sem_der._value == MAX_BABUINOS:
        sem_izq.acquire()
        cruzar("Cruzando hacia la izquierda")
        sem_izq.release()
    elif sem_izq._value == MAX_BABUINOS:
        sem_der.acquire()
        cruzar("Cruzando hacia la derecha")
        sem_der.release()

    semaforo.release()


def cruzar(st):
    print(st)
    time.sleep(random.randint(1, 2))


def main():
    if len(sys.argv) != 3:
        print("""Por favor provea dos argumentos:
                N (babuinos que cruzan de izquierda a derecha)
                M (babuinos que cruzan de derecha a izquierda)""")
        return

    N = int(sys.argv[1])
    M = int(sys.argv[2])

    babuinos(N, M)


if __name__ == "__main__":
    main()
