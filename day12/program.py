import argparse
import numpy as np
import scipy as sp
import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    graph = {}
    for s,e in map(lambda l : tuple(l.split('-')),i):
        if s in graph:
            graph[s].add(e)
        else:
            graph[s] = set((e,))
        if e in graph:
            graph[e].add(s)
        else:
            graph[e] = set((s,))
    return graph

def part1(i):
    graph = parse(i)
    all_paths = []
    def traverse(snode, cpath):
        if not snode.isupper() and snode in cpath:
            return

        cpath.append(snode)
        if snode == 'end':
            all_paths.append(cpath.copy())
        else:
            for nnode in graph[snode]:
                traverse(nnode, cpath)
        cpath.pop()

    traverse('start',[])
    print(len(all_paths))


def part2(i):
    graph = parse(i)
    all_paths = []
    def traverse(snode, cpath, double_visit):
        if not snode.isupper() and snode in cpath:
            if double_visit or snode == 'start':
                return
            else:
                double_visit = True
        cpath.append(snode)
        if snode == 'end':
            all_paths.append(cpath.copy())
        else:
            for nnode in graph[snode]:
                traverse(nnode, cpath, double_visit)
        cpath.pop()

    traverse('start',[], False)
    #print('\n'.join(list(map(','.join, all_paths))))
    print(len(all_paths))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


