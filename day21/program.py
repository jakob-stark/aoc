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
    ty = np.uint64

    pp1, pp2 = list(parse(i))
    pp1, pp2 = pp1-1, pp2-1

    uni = np.zeros((10,10,31,31), dtype=ty)
    uni[pp1,pp2,0,0] = 1

    dist = np.array((0,0,0,1,3,6,7,6,3,1),dtype=ty)
    plwin = np.array((0,0), dtype=ty)

    def cyclic_convolve(a):
        return np.sum(np.pad(np.convolve(a,dist), (0,1), constant_values=0).reshape((2,-1)), axis=0)

    c = np.array(((0,0,0,1,3,6,7,6,3,1),
                  (1,0,0,0,1,3,6,7,6,3),
                  (3,1,0,0,0,1,3,6,7,6),
                  (6,3,1,0,0,0,1,3,6,7),
                  (7,6,3,1,0,0,0,1,3,6),
                  (6,7,6,3,1,0,0,0,1,3),
                  (3,6,7,6,3,1,0,0,0,1),
                  (1,3,6,7,6,3,1,0,0,0),
                  (0,1,3,6,7,6,3,1,0,0),
                  (0,0,1,3,6,7,6,3,1,0))).transpose()
    def cyclic_convolvex(a):
        return np.einsum('ij,j->i', c, a)



    #print(cyclic_convolvex(dist))
    #print(cyclic_convolve(dist))

    def calc_points(u,pl):
        res = u.copy()
        res[:,:,:21,:21] = 0
        if pl == 0:
            for i, j, k, l in np.ndindex((10,10,21,21)):
                res[i,j,k+i+1,l] += u[i,j,k,l]
        else:
            for i, j, k, l in np.ndindex((10,10,21,21)):
                res[i,j,k,l+j+1] += u[i,j,k,l]
        return res

    t = iter(it.cycle((0,1)))
    while np.count_nonzero(uni[:,:,:21,:21]) > 0:
        pl = next(t)
        uni[:,:,:21,:21] = np.apply_along_axis(cyclic_convolve, pl, uni[:,:,:21,:21])
        uni = calc_points(uni,pl)

    w1 = np.sum(uni[:,:,21:,:])
    w2 = np.sum(uni[:,:,:,21:])
    print(max(w1,w2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


