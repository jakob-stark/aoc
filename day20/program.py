import argparse
import re
import numpy as np
#import scipy as sp
#import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    enh = np.array(list(i[0].translate(str.maketrans({'#':1,'.':0})).encode()),dtype=int)
    img = np.array(list(map(lambda l: list(l.translate(str.maketrans({'#':1,'.':0})).encode()), i[2:])),dtype=int)
    return enh, img


def part1(i, p1=True):
    class infarray:
        def __init__(self, a):
            self.a = a
            self.inf = 0

        def get(self, idx):
            try:
                return self.a[idx]
            except IndexError:
                return self.inf

        def set(self, idx, val):
            try:
                self.a[idx] = val
            except IndexError:
                self.inf = val

        def __str__(self):
            r = []
            for l in self.a:
                r.append(''.join(map(lambda t: {0:'.',1:'#'}[t], l)))
            r.append({0:'.',1:'#'}[self.inf])
            return '\n'.join(r)

    enh, img = parse(i)
    img = infarray(np.pad(img, 5 if p1 else 55, constant_values=0))
    to_bin = [int(2**x) for x in reversed(range(9))]

    for i in range(2 if p1 else 50):
        output = infarray(np.zeros_like(img.a))
        for x,y in np.ndindex(img.a.shape):
            v =  enh[sum(b * img.get((x-1+i//3, y-1+i%3)) for i,b in enumerate(to_bin))]
            output.set((x,y),v)
        output.set((np.nan,np.nan), enh[sum(b*img.get((np.nan,np.nan)) for b in to_bin)])
        img = output

    #print(img)
    print(np.count_nonzero(img.a))


def part2(i):
    part1(i,p1=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


