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

    print(c)
    print(plsco)
    print(c*min(plsco))


def part2(i):
    ty = np.float128

    pp1, pp2 = list(parse(i))
    pp1, pp2 = pp1-1, pp2-1
    #pp1, pp2 = 0,0

    #uni = np.zeros((10,10,40,40), dtype=ty)
    #uni[pp1,pp2,0,0] = 1

    mat = [ np.zeros((40,10), dtype=ty) for p in range(2) ]
    mat[0][0,pp1] = 1
    mat[1][0,pp2] = 1

    dist = np.array((0,0,0,1,3,6,7,6,3,1),dtype=ty)
    plwin = np.array((0,0), dtype=ty)

    def cyclic_convolve(a,b):
        return np.sum(np.pad(np.convolve(a,b), (0,1), constant_values=0).reshape((2,-1)), axis=0)
    cyclic_convolve = np.vectorize(cyclic_convolve, signature='(n),(n)->(n)')

    def calc_points(m):
        res = np.zeros_like(m)
        for i, j in np.ndindex(m.shape):
            if m[i,j] > 0:
                res[i+j+1,j] += m[i,j]
        return res

    t = iter(it.cycle(((0,1),(1,0))))
    while np.count_nonzero(mat[0]) > 0 or np.count_nonzero(mat[1]) > 0:
        #for i in range(21):
        pl, ot = next(t)

        mat[pl] = cyclic_convolve(mat[pl], dist)
        mat[pl] = calc_points(mat[pl])
        mat[ot] = 27*mat[ot]

        won = np.sum(mat[pl][21:,:])
        total = np.sum(mat[pl])

        mat[pl][21:,:] = 0
        mat[ot] = np.around((mat[ot]*(total-won)/total))
        #print(np.sum(mat[pl]))
        #print(np.sum(mat[ot]))

        #print(mat[pl])

        plwin[pl] += won
        #plwin[pl] += np.sum(mat[pl][21:,:])
        #mat[pl][21:,:] = 0

    print(np.max(plwin.astype(np.uint64)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


