import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# CPU-bound задача: вычисление чисел Фибоначчи (нагружает CPU)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

# IO-bound задача: эмуляция чтения данных (нагружает IO)
def io_task(lock, barrier, thread_id):
    time.sleep(1)  # Эмуляция задержки IO (например, запрос к БД)
    
    with lock:  # Потокобезопасное обновление данных
        print(f"Thread {thread_id} completed IO task.")

    barrier.wait()  # Ожидание всех потоков

# CPU-bound исполнение (используем процессы)
def cpu_bound_execution():
    print("Starting CPU-bound tasks...")
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(fib, [30, 31, 32, 33]))  # Четыре процесса
    print("CPU-bound tasks completed:", results)

# IO-bound исполнение (используем потоки)
def io_bound_execution():
    print("Starting IO-bound tasks...")
    lock = threading.Lock()
    barrier = threading.Barrier(4)  # Синхронизируем 4 потока

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(io_task, lock, barrier, i) for i in range(4)]
        for f in futures:
            f.result()  # Дожидаемся завершения всех потоков

    print("IO-bound tasks completed.")

if __name__ == "__main__":
    start = time.time()
    
    # Запускаем конкурентно обе задачи
    t1 = threading.Thread(target=io_bound_execution)
    t2 = multiprocessing.Process(target=cpu_bound_execution)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Total execution time: {time.time() - start:.2f} seconds")
