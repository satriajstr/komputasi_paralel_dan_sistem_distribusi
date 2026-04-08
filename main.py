import time
import random
from multiprocessing import Process, Queue

def task_execution(task_id):
    duration = random.uniform(0.5, 2.0) 
    time.sleep(duration)
    return (task_id, duration)

def static_worker(tasks, result_queue):
    total_time = 0
    for task in tasks:
        start = time.time()
        _, duration = task_execution(task)
        total_time += duration
    result_queue.put(total_time)

def static_distribution(num_tasks, num_workers):
    tasks = list(range(num_tasks))
    chunk_size = num_tasks // num_workers

    result_queue = Queue()
    processes = []

    start_time = time.time()

    for i in range(num_workers):
        chunk = tasks[i * chunk_size:(i + 1) * chunk_size]
        p = Process(target=static_worker, args=(chunk, result_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    total_execution = time.time() - start_time

    print("\n[STATIC DISTRIBUTION]")
    print("Ideal distribution tercapai jika semua worker selesai hampir bersamaan.")
    print(f"Total waktu eksekusi: {total_execution:.2f} detik")

def dynamic_worker(task_queue, result_queue):
    while not task_queue.empty():
        try:
            task = task_queue.get_nowait()
        except:
            break
        start = time.time()
        _, duration = task_execution(task)
        result_queue.put(duration)

def dynamic_distribution(num_tasks, num_workers):
    task_queue = Queue()
    result_queue = Queue()

    for i in range(num_tasks):
        task_queue.put(i)

    processes = []

    start_time = time.time()

    for _ in range(num_workers):
        p = Process(target=dynamic_worker, args=(task_queue, result_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    total_execution = time.time() - start_time

    print("\n[DYNAMIC DISTRIBUTION]")
    print("Optimal time tercapai saat semua worker selalu sibuk tanpa idle.")
    print(f"Total waktu eksekusi: {total_execution:.2f} detik")

if __name__ == "__main__":
    NUM_TASKS = 20
    NUM_WORKERS = 4

    static_distribution(NUM_TASKS, NUM_WORKERS)
    dynamic_distribution(NUM_TASKS, NUM_WORKERS)