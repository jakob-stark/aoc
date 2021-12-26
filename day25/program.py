import argparse
import numpy as np
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(inp):
    return np.array(tuple(map(lambda l: tuple(map(lambda f: {'.':0,'>':1,'v':2}[f], l)), inp)),dtype=int)

def part1(i,p1=True):
    field = parse(i)

    def move(field):
        moved = False

        dest = np.logical_and(np.roll(field == 1, 1, axis=1),field == 0)
        src  = np.roll(dest, -1, axis=1)
        field[dest] = 1
        field[src] = 0
        moved = moved or np.any(dest)

        dest = np.logical_and(np.roll(field == 2, 1, axis=0),field == 0)
        src  = np.roll(dest, -1, axis=0)
        field[dest] = 2
        field[src] = 0
        moved = moved or np.any(dest)
        return moved

    def pf(field):
        print('\n'.join(map(lambda l: ''.join(map(lambda f: {0:'.',1:'>',2:'v'}[f], l)), field)))

    #pf(field)
    x = 1
    while move(field):
        x += 1
    print(x)
    #pf(field)


def part2(i):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


