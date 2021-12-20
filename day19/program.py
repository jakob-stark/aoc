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

def scanner_rotation():
    def make_all():
        for i, j, k in it.permutations((0,1,2)):
            for s, t, u in it.product((1,-1),repeat=3):
                M = np.zeros((3,3),dtype=int)
                M[0,i] = s
                M[1,j] = t
                M[2,k] = u
                if np.linalg.det(M) == 1:
                    yield M
    return np.unique(np.array(list(make_all())),axis=0)

class Scanner:
    rotations = scanner_rotation()

    def __init__(self, n, beacons):
        self.n = n
        self.beacons = np.pad(beacons,((0,0),(0,1)),constant_values=1)

        self.distances = []
        self.distance_idx = []
        for i,j in it.combinations(range(len(self.beacons)), 2):
            b1, b2 = self.beacons[i], self.beacons[j]
            self.distances.append(np.sum(np.square(b1-b2)))
            self.distance_idx.append((i,j))
        self.distances = np.array(self.distances)

        self.reset_transformation()
        self.fixed = False

    def match_any(self, other):

        # discard if not more than 66 (12*11) distances are equal
        if 66 > sum((np.count_nonzero(other.distances == d) for d in self.distances)):
            return False

        other.reset_transformation()
        sb = self.get_beacons()
        ob = other.get_beacons()

        # try to calculate transformation with four points
        M = []
        N = []
        for u, d in enumerate(self.distances):
            if v := np.argmax(other.distances == d):
                i, j = self.distance_idx[u]
                k, l = other.distance_idx[v]
                if not (i in M or j in M or k in N or l in N):
                    M.append(i)
                    N.append(k)
                    M.append(j)
                    N.append(l)
            if len(M) == 4:
                break

        for p in ((0,1,2,3),(1,0,2,3),(0,1,3,2),(1,0,3,2)):
            Ma = np.array([sb[M[i]] for i in p], dtype=int)
            Na = np.array([ob[i] for i in N], dtype=int)

            try:
                #other.transformation = np.around(np.linalg.solve(Na,Ma).transpose()).astype(int)
                X, _, _, _ = np.linalg.lstsq(Na,Ma,rcond=-1)
                other.transformation = np.around(X.transpose()).astype(int)
                obtmp = other.get_beacons()
                if ( len(np.unique(sb, axis=0)) +
                     len(np.unique(obtmp, axis=0)) >=
                     len(np.unique(np.concatenate((sb,obtmp)), axis=0)) +
                     12 ):
                    return True
            except:
                pass
        
        # bruteforce by trying to match each point with each point of the other scanner
        other.reset_transformation()
        for rot in self.rotations:
            other.set_rotation(rot)
            other.set_position((0,0,0))
            ob = other.get_beacons()
            for s in sb:
                for o in ob:
                    other.set_position((s-o)[:3])
                    obtmp = other.get_beacons()
                    if ( len(np.unique(sb, axis=0)) +
                         len(np.unique(obtmp, axis=0)) >=
                         len(np.unique(np.concatenate((sb,obtmp)), axis=0)) +
                         12 ):
                        return True
        return False

    def manhattan(self,other):
        return np.sum(np.abs(self.get_position() - other.get_position()))

    def reset_transformation(self):
        self.transformation = np.eye(4,dtype=int)

    def set_position(self, pos):
        self.transformation[:3,3] = pos

    def get_position(self):
        return self.transformation[:3,3]

    def set_rotation(self, rot):
        self.transformation[:3,:3] = rot

    def get_rotation(self):
        return self.transformation[:3,:3]

    def fix(self):
        self.fixed = True

    def get_beacons(self):
        return np.einsum('ij,lj->li', self.transformation, self.beacons)


def part1(i, p1 = True):
    scanner_beacons = parse(i)
    u_scanners = [Scanner(n,b) for n,b in scanner_beacons.items()]
    f_scanners = [u_scanners.pop(0)]

    while u_scanners:
        u = u_scanners.pop(0)
        #print('trying scanner {}'.format(u.n))
        match = False
        for f in f_scanners:
            if f.match_any(u):
                #print('matched scanner {} at {}'.format(u.n, u.get_position()))
                match = True
                break
        if match:
            u.fix()
            f_scanners.insert(0,u)
        else:
            u_scanners.append(u)
    if p1:
        beacons = np.unique(np.concatenate([f.get_beacons() for f in f_scanners], axis=0), axis=0)
        print(len(beacons))
    else:
        print(max(map(lambda t: t[0].manhattan(t[1]), it.combinations(f_scanners, 2))))


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


