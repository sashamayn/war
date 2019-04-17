#! /usr/bin/env python3
import os
import multiprocessing as mp
from perm_unique import perm_unique

LOWEST_NUMBER = 1               # Inclusive
HIGHEST_NUMBER = 5              # Inclusive
N_DUPLICATES = 3
CHUNKSIZE = 100000              # Report after every chunk
POOL_SIZE = os.cpu_count() - 1  # Number of (additional) processes to use


# For-loops have a (very) small overhead,
# this was my attempt at removing it, but
# it didn't help much. I didn't feel like
# putting it back the way it was because
# I'm lazy and want to have some lunch. :)
def write_to(fd, mid):
    def inner(seq):
        fd.write("{}\n{}\n\n".format(
            " ".join(seq[:mid]),  # I'm splitting like this to not create an
            " ".join(seq[mid:]),  # additional list (of two lists) every time
        ))
    return inner


def run_and_report(iterable, msg=''):
    count = 0
    for _ in iterable:
        count += 1
        if not count % CHUNKSIZE:
            print(msg, count, sep='')
    print(msg, "Total: ", count, sep='')


def async_func(start, rest, filename, mid):
    # pid = mp.current_process().pid
    uid = ''.join(start)
    perms = map(lambda x: start + x, perm_unique(rest))
    with open(filename.format(uid), 'w') as fd:
        write_all = map(write_to(fd, mid), perms)
        run_and_report(write_all, f'{uid} ')


if __name__ == '__main__':
    flat_list = [
        str(item)  # If we already convert here, we don't have to convert for
                   # every permutation
        for item in range(LOWEST_NUMBER, HIGHEST_NUMBER + 1)
        for _ in range(N_DUPLICATES)
    ]

    mid = len(flat_list) // 2

    starts, rests = [], []
    for v in set(flat_list):
        starts.append((v,))
        copy = flat_list.copy()
        copy.remove(v)
        rests.append(tuple(copy))
    assert len(set(starts)) == len(starts)
    assert len(set(rests)) == len(rests)

    pool = mp.Pool(POOL_SIZE)
    for start, rest in zip(starts, rests):
        pool.apply_async(async_func, (start, rest, 'file-{}.txt', mid))
    pool.close()
    pool.join()
    # async_func((), flat_list, 'file-{}.txt', mid)

    # print("before perms")
    # perms = perm_unique(flat_list)
    # print("after perms")

    # with open('file.txt', 'w') as wr:
    #     run_and_report(map(write_to(wr, mid), perms))
    print("Done!")

# Four minutes
# 57 220 000
