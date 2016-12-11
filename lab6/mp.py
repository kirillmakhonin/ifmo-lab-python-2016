import argparse
import os
from itertools import takewhile, repeat
from multiprocessing import Process, Value, Array, cpu_count, Queue
from queue import Empty
from functools import reduce
from typing import Callable


def get_arguments() -> dict():
    parser = argparse.ArgumentParser(description='Calculate in multithreading mode')
    parser.add_argument('file', type=str)

    args = parser.parse_args()
    if not os.path.exists(args.file):
        parser.error('File doesnt exists: %s' % (args.file))
    else:
        return args


def file_lines_count(filename: str) -> int:
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen) + 1


def calculation(results_per_line: Array, queue: Queue, f1: Callable[[int, int], int]) -> None:
    while True:
        try:
            i, a, b = queue.get(True, 1)
            results_per_line[i] = f1(a, b)
        except Empty:
            print('Queue is empty. finishing')
            break
        except KeyboardInterrupt:
            print('Calculation interrupted from keyboard')
            break


def file_reading(path_to_file: str, queue: Queue) -> None:
    try:
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                a, b = (int(i) for i in line.split(' '))
                queue.put([i, a, b])
    except KeyboardInterrupt:
        print('File reading interrupted from keyboard')


def calculate_result(results_per_line: Array, f2: Callable[[int, int], int], result: int) -> None:
    result.value = reduce(f2, results_per_line, 0)


def calculate(path_to_file: str, f1: Callable[[int, int], int], f2: Callable[[int, int], int]) -> object:
    count_of_lines = file_lines_count(path_to_file)
    results_per_line = Array('i', range(count_of_lines))
    processes = list()
    data_queue = Queue() # line_no, a, b
    result = Value('i', 0)

    print('Entire lines count is %d' % count_of_lines)

    reading_process = Process(target=file_reading, args=(path_to_file, data_queue))
    reading_process.start()

    count_of_born_processes = min(cpu_count(), count_of_lines)
    for cpu_id in range(count_of_born_processes):
        print('Processor #%d. Starting child...' % cpu_id)
        p = Process(target=calculation, args=(results_per_line, data_queue, f1))
        p.start()
        processes.append(p)

    reading_process.join()
    print('Reading task has been finished')

    for p in processes:
        p.join()

    print('Calculation task has been finished')

    calculate_result_process = Process(target=calculate_result, args=(results_per_line, f2, result))
    calculate_result_process.start()
    calculate_result_process.join()
    return result.value

if __name__ == '__main__':
    try:
        args = get_arguments()

        f1 = lambda a, b: a - b
        f2 = lambda a, b: a + b

        result = calculate(args.file, f1, f2)
        print(result)
    except KeyboardInterrupt:
        print('Process interrupted')
        os.system('kill %d' % os.getpid())