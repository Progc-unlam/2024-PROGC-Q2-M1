import sys
import threading
import time
import random


def babuinos(N, M):
    semaforo = threading.Semaphore(5)
    mutex_izq = threading.Lock()
    mutex_der = threading.Lock()
    babuinos = []

    for _ in range(N):
        babuinos.append(threading.Thread(target=cruzar_soga, args=(
            semaforo, mutex_izq, mutex_der, True)))

    for _ in range(M):
        babuinos.append(threading.Thread(target=cruzar_soga, args=(
            semaforo, mutex_izq, mutex_der, False)))

    # No necesariamente arrancan todos los que quieren ir a la izquierda y luego todos los que quieren ir a la derecha
    random.shuffle(babuinos)
    for babuino in babuinos:
        babuino.start()
        # No todos los babuinos empiezan al mismo tiempo
        time.sleep(random.randint(1, 2))


def cruzar_soga(semaforo, mutex_izq, mutex_der,  es_izquierda):
    semaforo.acquire()
    if es_izquierda and not mutex_der.locked():
        if not mutex_izq.locked():
            mutex_izq.acquire()
            cruzar("Cruza hacia la izquierda")
            mutex_izq.release()
        else:
            cruzar("Cruza hacia la izquierda")
    elif not mutex_izq.locked():
        if not mutex_der.locked():
            mutex_der.acquire()
            cruzar("Cruza hacia la derecha")
            mutex_der.release()
        else:
            cruzar("Cruza hacia la derecha")
    semaforo.release()


def cruzar(st):
    print(st)
    # No todos los babuinos cruzan a la misma velocidad
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
