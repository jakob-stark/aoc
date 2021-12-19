import argparse
import numpy as np
import re
#import scipy as sp
#import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    scanners = {}
    s = 0
    for l in i:
        if not l:
            continue
        if x := re.match('--- scanner ([0-9]+) ---',l):
            s = x.group(1)
            scanners[s] = []
        else:
            scanners[s].append(l.split(','))
    return {s: np.array(k, dtype=int) for s,k in scanners.items()}


class Scanner:
    def __init__(self, beacons, transformation=None):
        self.beacons = beacons
        if transformation is None:
            self.transformation = np.eye(4)
        else:
            self.transformation = transformation

    def match(self, other):



def scanner_rotation():
    def make_permutations():
        for facing in (1,-1):
            for rotation in (((1,0),(0,1)),((0,1),(-1,0)),((-1,0),(0,-1)),((0,-1),(1,0))):
                for x,y,z in ((0,1,2),(1,2,0),(2,0,1)):
                    M = np.zeros((3,3))
                    M[x,x] = rotation[0][0]
                    M[x,y] = rotation[0][1]
                    M[y,x] = rotation[1][0]
                    M[y,y] = rotation[1][1]
                    M[z,z] = facing
                    yield M
    return np.unique(np.array(list(make_permutations())),axis=0)


def part1(i):
    scanner_beacons = parse(i)
    scanners = scanner_beacons.keys()
    scanner_pos = {scanners[0] : (0,0,0)}
    known_scanners = set(scanners[0:1])
    unknown_scanners = set(scanners[1:])
    print(scanners)


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


