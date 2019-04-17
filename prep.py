#! /usr/bin/env python3
"""
Find all unique starting combinations of a specified set of cards.
"""

import os
import multiprocessing as mp
from perm_unique import perm_unique


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


def run_and_report(iterable, chunksize, msg=''):
    count = 0
    for _ in iterable:
        count += 1
        if not count % chunksize:
            print(msg, count, sep='')
    print(msg, "Total: ", count, sep='')


def async_func(start, rest, filename, mid, chunksize):
    # pid = mp.current_process().pid
    uid = ''.join(start)
    perms = map(lambda x: start + x, perm_unique(rest))
    with open(filename.format(uid), 'w') as fd:
        write_all = map(write_to(fd, mid), perms)
        run_and_report(write_all, chunksize, f'{uid} ')


def main(args=[]):
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        'highest_card',
        type=int,
        help="The value of the highest card in the deck.")
    parser.add_argument(
        'n_duplicates',
        type=int,
        help="The number of suits,"
        " i.e. the number of times every unique value appears.")
    parser.add_argument(
        '--lowest_card',
        default=1,
        type=int,
        help="The value of the lowest card in the deck.")
    parser.add_argument(
        '--chunksize',
        default=100000,
        type=int,
        help="Print how many configurations have been generated every"
        " `chunksize` configurations.")
    parser.add_argument(
        '--pool_size',
        default=os.cpu_count() - 1,
        type=int,
        help="Number of (additional) processes to use."
    )

    args = parser.parse_args(args)

    flat_list = [
        str(item)  # If we already convert here, we don't have to convert for
                   # every permutation
        for item in range(args.lowest_card, args.highest_card + 1)
        for _ in range(args.n_duplicates)
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

    pool = mp.Pool(args.pool_size)
    try:
        for start, rest in zip(starts, rests):
            pool.apply_async(
                async_func,
                (start, rest, 'file-{}.txt', mid, args.chunksize))
        pool.close()
        pool.join()
    finally:
        pool.terminate()

    # async_func((), flat_list, 'file-{}.txt', mid)

    # print("before perms")
    # perms = perm_unique(flat_list)
    # print("after perms")

    # with open('file.txt', 'w') as wr:
    #     run_and_report(map(write_to(wr, mid), perms))
    print("Done!")


if __name__ == '__main__':
    main()
