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
            self.vol = tuple(map(lambda s: tuple(map(int,s.split('=')[1].split('..'))), vol.split(',')))
            self.vol = tuple(map(lambda p: (p[0], p[1]+1), self.vol))
        else:
            self.on = True
            self.vol = ((0,0),(0,0),(0,0))

    def get_coordinates(self):
        return tuple(it.chain(*self.vol))

    def __repr__(self):
        return 'Instruction({},{})'.format(self.on,self.vol)


class Cube:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = min(x1,x2)
        self.x2 = max(x2,x1)
        self.y1 = min(y1,y2)
        self.y2 = max(y2,y1)
        self.z1 = min(z1,z2)
        self.z2 = max(z2,z1)

    def inside(self,other):
        return ( other.x1 <= self.x1 and
                 self.x2 <= other.x2 and
                 other.y1 <= self.y1 and
                 self.y2 <= other.y2 and
                 other.z1 <= self.z1 and
                 self.z2 <= other.z2 )

    def overlap(self,other):
        return not ( self.x2 <= other.x1 or
                     self.x1 >= other.x2 or
                     self.y2 <= other.y1 or
                     self.y1 >= other.y2 or
                     self.z2 <= other.z1 or
                     self.z1 >= other.z2 )

    def connected(self,other):
        return not ( self.x2 < other.x1 or
                     self.x1 > other.x2 or
                     self.y2 < other.y1 or
                     self.y1 > other.y2 or
                     self.z2 < other.z1 or
                     self.z1 > other.z2 )

    def get_coordinates(self):
        return (self.x1, self.x2, self.y1, self.y2, self.z1, self.z2)

    def get_xspan(self):
        return (self.x1, self.x2)

    def get_yspan(self):
        return (self.y1, self.y2)

    def get_zspan(self):
        return (self.z1, self.z2)

    def get_volume(self):
        return (self.x2-self.x1)*(self.y2-self.y1)*(self.z2-self.z1)

    def __repr__(self):
        return 'Cube{}'.format(self.get_coordinates())

    def __eq__(self,other):
        return self.get_coordinates() == other.get_coordinates()

    def __hash__(self):
        return hash(self.get_coordinates)


class CubeSet:
    def __init__(self, cubes=[]):
        self.cubes = set()
        for c in cubes:
            self.add_cube(c)

    def add_cube_int(self,c):
        ncubes = set()
        fcubes = set()
        for b in self.cubes:
            if b.overlap(c):
                fcubes.add(b)
            else:
                ncubes.add(b)

        x = sorted(it.chain(*([b.get_xspan() for b in fcubes]+[c.get_xspan()])))
        y = sorted(it.chain(*([b.get_yspan() for b in fcubes]+[c.get_yspan()])))
        z = sorted(it.chain(*([b.get_zspan() for b in fcubes]+[c.get_zspan()])))
        for i,j,k in it.product(range(len(fcubes)*2+1), repeat=3):
            t = Cube(x[i],x[i+1],y[j],y[j+1],z[k],z[k+1])
            if any((t.inside(b) for b in fcubes)) or t.inside(c):
                ncubes.add(t)
        self.cubes = ncubes

    def simplify(self):
        ncubes = set()
        while len(self.cubes) > 0:
            b = self.cubes.pop()
            while True:
                merged = False
                for a in self.cubes:
                    if b.x1 == a.x1 and b.x2 == a.x2 and a.y1 == b.y1 and a.y2 == b.y2 and b.connected(a):
                        b = Cube(b.x1,b.x2,b.y1,b.y2,min(b.z1,a.z1),max(b.z2,a.z2))
                        self.cubes.remove(a)
                        merged = True
                        break
                    if b.y1 == a.y1 and b.y2 == a.y2 and a.z1 == b.z1 and a.z2 == b.z2 and b.connected(a):
                        b = Cube(min(b.x1,a.x1),max(b.x2,a.x2),b.y1,b.y2,b.z1,b.z2)
                        self.cubes.remove(a)
                        merged = True
                        break
                    if b.x1 == a.x1 and b.x2 == a.x2 and a.z1 == b.z1 and a.z2 == b.z2 and b.connected(a):
                        b = Cube(b.x1,b.x2,min(b.y1,a.y1),max(b.y2,a.y2),b.z1,b.z2)
                        self.cubes.remove(a)
                        merged = True
                        break
                if not merged:
                    ncubes.add(b)
                    break
        self.cubes = ncubes
                    

    def add_cube(self,c):
        self.add_cube_int(c)
        self.simplify()

    def remove_cube(self, c):
        self.add_cube_int(c)
        self.cubes = {b for b in self.cubes if not b.inside(c)}
        self.simplify()

    def get_volume(self):
        return sum((b.get_volume() for b in self.cubes))

def parse(i):
    return list(map(Instruction, i))

def part1(i, p1=True):
    instructions = parse(i)
    cs = CubeSet()
    for inst in instructions:
        if (not p1) or all((-50 <= c <= 50 for c in inst.get_coordinates())):
            print(inst)
            if inst.on:
                cs.add_cube(Cube(*inst.get_coordinates()))
            else:
                cs.remove_cube(Cube(*inst.get_coordinates()))
    print(cs.cubes)
    print(cs.get_volume())

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


