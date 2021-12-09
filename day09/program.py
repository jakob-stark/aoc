import argparse
import numpy as np
import scipy as sp
import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    tmp = tuple(map(lambda t: (9,)+tuple(map(int,t))+(9,), map(tuple,i)))
    return np.array(((9,)*len(tmp[0]),) + tmp + ((9,)*len(tmp[0]),),dtype=int)

def part1(i):
    hm = parse(i)
    sum_rl = 0
    for x,y in np.ndindex(hm[1:-1,1:-1].shape):
        low_point = True
        for xoff, yoff in ((1,0),(-1,0),(0,1),(0,-1)):
            if hm[x+1,y+1] >= hm[x+1+xoff,y+1+yoff]:
                low_point = False
        if low_point:
            sum_rl += hm[x+1,y+1]+1
    print(sum_rl)


def part2(i):
    hm = parse(i)
    hm[hm != 9] = 1
    hm[hm == 9] = 0
    cl, num = si.label(hm)
    basins,_ = np.histogram(cl,bins=np.arange(1,num+2))
    print(np.product(np.sort(basins)[-3:]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


