import argparse as ap
import numpy as np
import functools as ft
import operator as op
import itertools as it

def read(f):
        return map(str.strip, f)

def part1(i):
    print(
        ft.reduce(op.mul,
            map( lambda s : int(''.join(map(str,s)),2),
                (lambda s : (1*(s > 0), 1*(s < 0)))(
                   sum( 
                        map( lambda s : 2*s-1,
                            map( lambda s : np.array(tuple(s),dtype=int),
                                i
                            )
                        )
                    )
                )
            )
        )
    )

def part2(i):
    class node:
        def __init__(self, depth):
            self.depth = depth
            if self.depth > 0:
                self.rchild = node(depth-1)
                self.lchild = node(depth-1)
            else:
                self.list = []

        def __len__(self):
            return len(self.rchild) + len(self.lchild) if self.depth > 0 else len(self.list)

        def insert(self, element):
            if self.depth > 0:
                if element[-self.depth]:
                    self.rchild.insert(element)
                else:
                    self.lchild.insert(element)
            else:
                self.list.append(element)

        def get_most_common(self):
            if self.depth > 0:
                if len(self.rchild) >= len(self.lchild):
                    return self.rchild.get_most_common()
                else:   
                    return self.lchild.get_most_common()
            else:
                return self.list;

        def get_least_common(self):
            if self.depth > 0:
                if len(self.rchild) == 0:
                    return self.lchild.get_least_common()
                elif len(self.lchild) == 0:
                    return self.rchild.get_least_common()
                elif len(self.rchild) < len(self.lchild):
                    return self.rchild.get_least_common()
                else:  
                    return self.lchild.get_least_common()
            else:
                return self.list;

        def __str__(self):
            if self.depth > 0:
                return '[ {}, {} ]'.format(str(self.rchild), str(self.lchild))
            else:
                return '[ list({}) ]'.format(len(self.list))
    
    a = list(map(lambda t : tuple(map(int,t)),map(tuple,i)))
    tree = node(len(a[0]))
    list(map(tree.insert, a))
    x = tree.get_most_common() + tree.get_least_common()
    print(ft.reduce(op.mul,map(lambda t: int(''.join(map(str,t)),2), x)))


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('-p', type=int, help='part of the day\'s challenge')
    parser.add_argument('-i', type=str, help='input file')
    args = parser.parse_args()
    with open(args.i) as f:
        if args.p == 1:
            part1(read(f))
        elif args.p == 2:
            part2(read(f))

