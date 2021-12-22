import argparse
import itertools as it
from ctypes import *

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

class Cube(Structure):
    _fields_ = [ ("x1", c_int),
                 ("x2", c_int),
                 ("y1", c_int),
                 ("y2", c_int),
                 ("z1", c_int),
                 ("z2", c_int),
                 ("on", c_byte) ]
    
def parse(inp):
    result = (Cube * len(inp))()
    for i, line in enumerate(inp):
        on, vol = line.split()
        result[i].on = {'on':1, 'off':0}[on]
        vol = tuple(map(lambda s: tuple(map(int,s.split('=')[1].split('..'))), vol.split(',')))
        result[i].x1, result[i].x2 = vol[0]
        result[i].y1, result[i].y2 = vol[1]
        result[i].z1, result[i].z2 = vol[2]
    return result

libi = CDLL('./integrate.so')
libi.integrate.restype = c_ulonglong

def part1(i, p1=True):
    cubes = parse(i)
    print(libi.integrate(pointer(cubes), len(cubes), int(p1)))
    return

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


