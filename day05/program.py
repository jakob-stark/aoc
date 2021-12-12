import argparse as ap
import numpy as np
import functools as ft
import operator as op
import itertools as it

def read(f):
    return map(str.strip, f)

def parse(i):
    return map(lambda s : tuple(map(lambda e : tuple(map(int,e.split(','))),s.split(' -> '))), i)

def part1(i):
    field = np.zeros((1000,1000),dtype=int)
    for (xs,ys),(xe,ye) in parse(i):
        if not (xs == xe or ys == ye):
            continue
        nsteps = max(abs(xe-xs),abs(ye-ys))
        for s in range(nsteps+1):
            x = int(xs + (xe-xs)/nsteps*s)
            y = int(ys + (ye-ys)/nsteps*s)
            field[y,x] += 1
    print(np.sum(field >= 2))

def part2(i):
    field = np.zeros((1000,1000),dtype=int)
    for (xs,ys),(xe,ye) in parse(i):
        nsteps = max(abs(xe-xs),abs(ye-ys))
        for s in range(nsteps+1):
            x = int(xs + (xe-xs)/nsteps*s)
            y = int(ys + (ye-ys)/nsteps*s)
            field[y,x] += 1
    print(np.sum(field >= 2))


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('-p', type=int, help='part of the day\'s challenge')
    parser.add_argument('-i', type=str, help='input file')
    args = parser.parse_args()
    with open(args.i) as f:
        if args.p == 1:
            part1(read(f))
        elif args.p == 2:
            part2(read(f))

