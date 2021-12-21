import argparse
import re
import numpy as np
#import scipy as sp
#import scipy.ndimage as si
import itertools as it
from scipy.fftpack import fft, ifft

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return tuple(map(lambda l: int(l.split(': ')[-1]), i))

def part1(i, p1=True):
    plpos = list(parse(i))
    plsco = [0,0]
    
    def det_die():
        die = iter(it.cycle(range(1,101)))
        while True:
            yield sum((next(die) for i in range(3)))
    
    def turn():
        return iter(it.cycle((0,1)))

    c = 0
    t = turn()
    d = det_die()
    while plsco[0] < 1000 and plsco[1] < 1000:
        pl = next(t)
        plpos[pl] = (plpos[pl] + next(d) - 1) % 10 + 1
        plsco[pl] += plpos[pl]
        c += 3

    #print(c)
    #print(plsco)
    print(c*min(plsco))


def part2(i):
    ty = np.uint64

    pp1, pp2 = list(parse(i))

    uni = np.zeros((10,22,10,22), dtype=ty)
    uni[pp1-1,0,pp2-1,0] = 1

    win = np.array((0,0), dtype=ty)

    c = np.array((0,0,0,1,3,6,7,6,3,1), dtype=ty)
    C = np.zeros((10,22,10,22),dtype=ty)
    for i,j in np.ndindex((21,10)):
        C[:,i,j,i] = np.roll(c,j)

    D = np.zeros((10,22,10,22),dtype=ty)
    for i, j in np.ndindex((10,21)):
        D[i,min(j+i+1,21),i,j] = 1

    T = np.einsum('ijkl,kluv->ijuv', D,C)

    t = iter(it.cycle((0,1)))
    while np.count_nonzero(uni[:,:21,:,:21]) > 0:
        uni = np.einsum('ijkl,klst->stij',T,uni)
        win[next(t)] += np.sum(uni[:,:21,:,21])

    print(np.max(win))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


