import argparse
import numpy as np
import scipy as sp
import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return np.array(tuple(map(lambda t: tuple(map(int,t)), map(tuple,i))),dtype=int)

def part1(i):
    field = parse(i)
    conv = np.array(((1,1,1),(1,1,1),(1,1,1)))

    num_flashed = 0
    for i in range(100):
        field = field + 1
        while np.any(field > 9):
            increase = si.convolve((field > 9).astype(int), conv, mode='constant')
            field[field > 9] = 0
            field[field != 0] += increase[field != 0]
        num_flashed += np.count_nonzero(field == 0)
    print(num_flashed)


def part2(i):
    field = parse(i)
    conv = np.array(((1,1,1),(1,1,1),(1,1,1)))

    for i in it.count():
        field = field + 1
        while np.any(field > 9):
            increase = si.convolve((field > 9).astype(int), conv, mode='constant')
            field[field > 9] = 0
            field[field != 0] += increase[field != 0]
        if np.all(field == 0):
            print(i+1)
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


