import argparse
from heapq import *
import numpy as np
import time
#import scipy as sp
#import scipy.ndimage as si
#import itertools as it
#import matplotlib.pyplot as plt

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

INF = 100000

def parse(i):
    return np.array(tuple(map(lambda l: tuple(map(int,l)), i)),dtype=int)


def astar(grid, h = None, ax = None):
    ts = time.time()
    start = (1,1)
    goal =  grid.shape
    grid = np.pad(grid, 1, constant_values=INF)

    if h:
        H = lambda p: h(p[0]-goal[0], p[1]-goal[1])
    else:
        H = None

    gscores = {start:0}
    if H:
        fscores = [(H(start),0, start)]
    else:
        fscores = [(0, start)]
    
    while len(fscores) > 0:
        if H:
            fcost, gcost, cpath = heappop(fscores)
        else:
            gcost, cpath = heappop(fscores)

        if gcost != gscores[cpath]:
            continue

        if cpath == goal:
            print(gcost)
            if ax:
                print(time.time()-ts)
                image = np.zeros_like(grid)
                for k in np.ndindex(image.shape):
                    image[k] = gscores.get(k, 0)
                ax.matshow(image[1:-1,1:-1])
            return
        
        for dx, dy in ((1,0),(0,1),(-1,0),(0,-1)):
            x, y = cpath
            nb = (x+dx, y+dy)
            gscore = gcost + grid[nb]
            if gscore < gscores.get(nb, INF):
                gscores[nb] = gscore
                if H:
                    heappush(fscores,(H(nb) + gscore, gscore, nb))
                else:
                    heappush(fscores,(gscore, nb))


def part1(i):
    grid = parse(i)
    #fig, (ax1, ax2) = plt.subplots(1,2)
    #astar(grid,h = None, ax=ax1)
    #astar(grid,h = lambda dx, dy: abs(dx)+abs(dy), ax=ax2)
    #plt.show()
    astar(grid)


def part2(i):
    multi = np.array(((0,1,2,3,4),
                      (1,2,3,4,5),
                      (2,3,4,5,6),
                      (3,4,5,6,7),
                      (4,5,6,7,8)))
    grid = parse(i)
    new_shape = (grid.shape[0]*5, grid.shape[1]*5)
    grid = (np.reshape(np.swapaxes(np.add.outer(multi, grid), 1,2), new_shape) - 1) % 9 + 1
    
    #fig, (ax1, ax2) = plt.subplots(1,2)
    #astar(grid,h = None, ax=ax1)
    #astar(grid,h = lambda dx, dy: abs(dx)+abs(dy), ax=ax2)
    #plt.show()
    astar(grid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


