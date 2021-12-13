import argparse
import numpy as np
import scipy as sp
import scipy.ndimage as si
import itertools as it
import matplotlib.pyplot as plt

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))


def get_reflection_matrix(a,b,m):
    R = np.array(((1-2*a*a, -2*a*b, 0),(-2*a*b, 1-2*b*b, 0),(0,0,1)))
    if a != 0:
        T = np.array(((1,0,m/a),(0,1,0),(0,0,1)))
    else:
        T = np.array(((1,0,0),(0,1,m/b),(0,0,1)))
    return np.einsum('ij,jk,kl->il',np.linalg.inv(T),R,T)


def parse(i):
    dots = []
    folds = []
    for l in i:
        if l:
            if 'fold' in l:
                folds.append((lambda f: (f[0],int(f[1]))) (l.split()[-1].split('=')))
            else:
                dots.append(tuple(map(int,l.split(','))))
    return dots, folds


def part1(i):
    dots, folds = parse(i)
    dots = np.pad(np.array(dots),((0,0),(0,1)),constant_values=1)

    for i, f in zip(range(1),folds):
        a,b = (-1,0) if f[0] == 'x' else (0,-1)
        m = f[1]
        line = np.array((a,b,m))
        M = get_reflection_matrix(a,b,m)

        dots = np.concatenate((dots, np.einsum('ij,kj->ki',M,dots)))
        dots = np.unique(dots[np.einsum('j,kj->k', line, dots) > 0], axis=0)
    print(len(dots))


def part2(i):
    dots, folds = parse(i)
    dots = np.pad(np.array(dots,dtype=int),((0,0),(0,1)),constant_values=1)

    for i, f in enumerate(folds):
        a,b = (-1,0) if f[0] == 'x' else (0,-1)
        m = f[1]
        line = np.array((a,b,m),dtype=int)
        M = get_reflection_matrix(a,b,m).astype(int)

        dots = np.concatenate((dots, np.einsum('ij,kj->ki',M,dots)))
        dots = np.unique(dots[np.einsum('j,kj->k', line, dots) > 0], axis=0)

    display = [['.']*np.max(dots[:,0]+1) for i in range(np.max(dots[:,1]+1))]
    for dot in dots:
        display[dot[1]][dot[0]] = '#'
    print('\n'.join(map(''.join,display)))



if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


