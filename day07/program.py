import argparse
import numpy as np

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return map(int,i[0].split(','))

def part1(i):
    x = np.array(list(parse(i)),dtype=int)
    print(np.sum(np.abs(x-np.median(x))).astype(int))

def part2(i):
    x = np.array(list(parse(i)),dtype=int)
    l = np.array([np.sum((np.abs(x-m)**2 + np.abs(x-m)) / 2 ).astype(int) for m in range(np.min(x),np.max(x)+1)])
    print(np.min(l))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


