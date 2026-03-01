import multiprocessing
import time
import random

N = 1000
A = [[random.randint(1, 10) for _ in range(N)] for _ in range(N)]
B = [[random.randint(1, 10) for _ in range(N)] for _ in range(N)]

def tambah_baris(i):
    return [A[i][j] + B[i][j] for j in range(N)]

if __name__ == "__main__":
    start = time.time()

    with multiprocessing.Pool() as pool:
        C = pool.map(tambah_baris, range(N))

    end = time.time()
    print("Waktu paralel:", end - start)