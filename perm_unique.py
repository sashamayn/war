"""
Code copy-pasted from https://stackoverflow.com/a/6285203/1171215

Essentially it gives all permutations, without the duplicates resulting from
duplicate values.
"""

import itertools as it

# When to stop trying to only produce unique options and instead produce all
# and then filter afterwards.
# If this is 0, it is the same as doing everything recursively.
# If this is bigger than the maximum length, it's the same as what you did
# before, i.e. generate everything and filter out what you don't want.
CUTOFF = 5  # This seems to be the sweet spot

# class UniqueElement:
#     def __init__(self, value, occurrences):
#         self.value = value
#         self.occurrences = occurrences


def perm_unique(elements):
    eset = set(elements)
    # Accessing lists elements is faster than attributes
    # listunique = [UniqueElement(i, elements.count(i)) for i in eset]
    listunique = [[i, elements.count(i)] for i in eset]
    u = len(elements)
    return perm_unique_helper(listunique, [0]*u, u-1)


def perm_unique_helper(listunique, result_list, d):
    # if d < 0:
        # yield tuple(result_list)
        # This re-uses the same memory, which should be faster, but is
        # dangerous if you want to use two at the same time (which we don't).
        # yield result_list
    if d < CUTOFF:
        # Now the number of duplicates is very small compared to the number of
        # "correct" values, making it more efficient to use the built-in
        # functions, instead of doing vary many unnecessary recursive calls
        # (which are slow because a function call in python has quite some
        # overhead).
        starts = set(it.permutations(
            [v for v, n in listunique for _ in range(n)]
        ))
        end = tuple(result_list[d+1:])
        for start in starts:
            yield start + end
    else:
        for i in listunique:
            if i[1] > 0:
                result_list[d] = i[0]
                i[1] -= 1
                yield from perm_unique_helper(listunique, result_list, d-1)
                i[1] += 1
