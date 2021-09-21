from __future__ import print_function
import timeit

import ulid2


def perftest():
    tmr = timeit.Timer(lambda: ulid2.generate_ulid_as_uuid())
    n_iterations = 300000
    time_taken = tmr.timeit(n_iterations)
    return int(n_iterations / time_taken)


def main():
    results = []
    for x in range(5):
        ops_per_sec = perftest()
        print(x + 1, " ... ", ops_per_sec)
        results.append(ops_per_sec)
    n_results = len(results)
    mean = sum(results) / n_results
    median = sorted(results)[n_results // 2]
    print("mean ops/sec  ", mean)
    print("median ops/sec", median)


if __name__ == '__main__':
    main()
