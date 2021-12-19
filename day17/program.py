import argparse
import numpy as np
#import scipy as sp
#import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return tuple(map(lambda x: tuple(map(int,x.split('=')[1].split('..'))), i[0].split(': ')[1].split(', ')))


def part1(i, p1=True):
    (xmin, xmax), (ymin, ymax) = parse(i)
    vy_min, vy_max = ymin-1, -ymin+1
    vx_min, vx_max = int((2*xmin)**0.5), xmax+1
    
    results = []
    for vx in range(vx_min, vx_max+1):
        for vy in range(vy_min, vy_max+1):
            x, y = 0,0
            Y = 0
            _vx, _vy = vx, vy
            while True:
                x += _vx
                y += _vy
                _vx = _vx if _vx == 0 else (_vx + 1 if _vx < 0 else _vx - 1)
                _vy -= 1
                if y > Y:
                    Y = y
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    results.append((Y, (vx, vy)))
                    break
                elif x > xmax or y < ymin:
                    break
    if p1:
        print(max(results, key = lambda e: e[0])[0])
    else:
        print(len(results))


def part2(i):
    part1(i,False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


