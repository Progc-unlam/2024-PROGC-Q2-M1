import sys
import threading
import time


class CharacterCounter:
    def __init__(self, lines):
        self.lines = lines
        self.rp = 0

    def count_characters(self):
        for line in self.lines:
            self.rp += len(line)

    def get_count(self):
        return self.rp


def validate_args():
    if len(sys.argv) != 3:
        return (None, None)

    return sys.argv[1], int(sys.argv[2])


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def main():
    file_path, nof_threads = validate_args()
    if not file_path:
        print("""Por favor provea dos argumentos: 
                - El nombre del archivo a procesar
                - La cantidad de hilos""")
        return

    print(f"Procesando archivo {file_path} con {nof_threads} hilos")

    lines = read_file(file_path).split('\n')
    nof_threads = min(nof_threads, len(lines))
    lines_per_thread = len(lines) // nof_threads
    rt = 0

    threads = []
    counters = []
    for i in range(nof_threads):
        start = i * lines_per_thread
        end = start + lines_per_thread
        if i == nof_threads - 1:
            end = len(lines)
        counter = CharacterCounter(lines[start:end])
        thread = threading.Thread(target=counter.count_characters)
        threads.append(thread)
        counters.append(counter)
        thread.start()

    for thread in threads:
        thread.join()

    for counter in counters:
        rt += counter.get_count()

    print(f"El archivo {file_path} tiene {rt} caracteres")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(
        f"Tiempo de ejecución: {(time.time() - start_time)*1000} milisegundos")
