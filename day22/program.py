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

class Instruction:
    def __init__(self, line=None):
        if line:
            on, vol = line.split()
            self.on = {'on':True, 'off':False}[on]
            vol = tuple(map(lambda s: tuple(map(int,s.split('=')[1].split('..'))), vol.split(',')))
            self.vol = tuple(map(lambda p: (p[0], p[1]+1), vol))
        else:
            self.on = True
            self.vol = ((0,0),(0,0),(0,0))
        (self.x1,self.x2),(self.y1,self.y2),(self.z1,self.z2) = self.vol

    def get_coordinates(self):
        return tuple(it.chain(*self.vol))

    def inside(self, x, y, z):
        return self.x1 <= x < self.x2 and self.y1 <= y < self.y2 and self.z1 <= z < self.z2

    def __repr__(self):
        return 'Instruction({},{})'.format(self.on,self.vol)


def parse(i):
    return list(map(Instruction, i))

def part1(i, p1=True):
    instructions = parse(i)
    x = np.array([[i.vol[0][0], i.vol[0][1]] for i in instructions], dtype=int).flatten()
    y = np.array([[i.vol[1][0], i.vol[1][1]] for i in instructions], dtype=int).flatten()
    z = np.array([[i.vol[2][0], i.vol[2][1]] for i in instructions], dtype=int).flatten()

    if p1:
        x = np.unique(x[np.abs(x) <= 51])
        y = np.unique(y[np.abs(y) <= 51])
        z = np.unique(z[np.abs(z) <= 51])
    else:
        x = np.unique(x)
        y = np.unique(y)
        z = np.unique(z)

    print(x)
    print(y)
    print(z)

    vol = 0
    s = (len(x)-1)*(len(y)-1)*(len(z)-1)/100000
    T = 0
    for t,(i,j,k) in enumerate(np.ndindex((len(x)-1,len(y)-1,len(z)-1))):
        if t > T:
            print(int(t/s))
            T += s
        on = False
        for inst in instructions:
            if inst.inside(x[i],y[j],z[k]):
                on = inst.on
        if on:
            vol += (x[i+1]-x[i]) * (y[j+1]-y[j]) * (z[k+1]-z[k])

    print(vol)

def part2(i):
    part1(i, p1=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


