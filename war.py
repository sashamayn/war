#! /usr/bin/env python3
import fileinput


def read_file():
    """
    Opens all files passed on the command-line.
    If no files were passed, reads from stdin.
    """
    with fileinput.input() as f:
        cur_tuple = []
        for line in f:
            if len(line) != 1:
                if len(cur_tuple) == 0:  # on the first
                    p0 = [int(x) for x in line.split()]
                    cur_tuple.append(p0)
                elif len(cur_tuple) == 1:
                    p1 = [int(x) for x in line.split()]
                    cur_tuple.append(p1)
                    # print(cur_tuple)
                    yield cur_tuple
                    cur_tuple = []


def calculate_game(p0, p1, tie_counter):
    cycle = False
    # set of sets?
    configurations = []
    init = [p0.copy(), p1.copy()]
    configurations.append(init)
    print(configurations)

    while len(p0) != 0 and len(p1) != 0:

        p0_old = p0
        p1_old = p1
        if p1[-1] < p0[-1]:
            # add to the beginning of deck
            p0_old.insert(0, p0[-1])
            p0_old.insert(0, p1[-1])
            p0 = p0_old[:-1]
            p1 = p1_old[:-1]

        elif p1[-1] > p0[-1]:
            p1_old.insert(0, p1[-1])
            p1_old.insert(0, p0[-1])
            p0 = p0_old[:-1]
            p1 = p1_old[:-1]

        # the equal case
        elif p1[-1] == p0[-1]:
            n = -1
            while p1[n] == p0[n] and min(len(p0), len(p1)) != abs(n):
                n -= 1

            if min(len(p0), len(p1)) > abs(n):
                if p1[n] > p0[n]:

                    p1 = p0_old[n:][::-1] + \
                        p1_old[n:][::-1] + \
                        p1_old[:len(p1_old)+n]
                    p0 = p0_old[:len(p0_old)+n]

                elif p1[n] < p0[n]:

                    p0 = p1_old[n:][::-1] + \
                        p0_old[n:][::-1] + \
                        p0_old[:len(p0_old)+n]
                    p1 = p1_old[:len(p1_old)+n]
            # tie
            elif min(len(p0), len(p1)) == abs(n):
                if p0 == p1:
                    tie_counter += 1
                break

            else:
                break

        cur = [p0.copy(), p1.copy()]

        if cur in configurations or cur[::-1] in configurations:
            print("cycle found!", cur)
            for c in configurations:
                print(c)
            cycle = True
            break
        else:
            configurations.append(cur)

    return cycle, tie_counter


# add cycle detection
def main():
    games = read_file()
    tie_counter = 0
    game_counter = 0

    for each in games:
        game_counter += 1
        p0, p1 = each
        cycle, tie_counter = calculate_game(p0, p1, tie_counter)
        if cycle:
            print("cycle!")
            break

    print(tie_counter, "out of", game_counter, "games end in ties")


if __name__ == '__main__':
    main()
