import argparse
import numpy as np
#import scipy as sp
#import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return [eval(l) for l in i]


class Number:

    def __init__(self, l):
        self.first = {'prev':None}
        self.root, self.last = self.fill(l, 0, self.first)
        self.first = self.first['next']
        self.first['prev'] = None

    def fill(self, l, d, p = {}, P = None):
        if type(l) is list:
            node = dict()
            node['parent'] = node
            node['left'], p = self.fill(l[0], d+1, p, node)
            node['right'] , p = self.fill(l[1], d+1, p, node)
            return node, p
        else:
            node = dict()
            node['parent'] = P
            node['value'] = l
            node['depth'] = d
            p['next'] = node
            node['prev'] = p
            node['next'] = None
            return node, node

    def as_list(self):
        def to_list(node):
            if not node.get('value', None) is None:
                return node['value']
            else:
                return [to_list(node['left']), to_list(node['right'])]
        return to_list(self.root)

    def magnitude(self):
        def to_mag(node):
            if not node.get('value', None) is None:
                return node['value']
            else:
                return 3*to_mag(node['left']) + 2*to_mag(node['right'])
        return to_mag(self.root)

    def reduce(self):
        it = self.first
        while not it is None:
            if it['depth'] > 4:
                if it['prev']:
                    it['prev']['value'] += it['value']
                    it['prev']['next'] = it['parent']
                else:
                    self.first = it['parent']
                if it['next']['next']:
                    it['next']['next']['value'] += it['next']['value']
                    it['next']['next']['prev'] = it['parent']
                else:
                    self.last = it['parent']
                it['parent']['left'] = None
                it['parent']['right'] = None
                it['parent']['value'] = 0
                it['parent']['depth'] = it['depth'] - 1
                it['parent']['prev'] = it['prev']
                it['parent']['next'] = it['next']['next']
                return True
            it = it['next']

        it = self.first
        while not it is None:
            if it['value'] >= 10:
                it['left'] = {'value': it['value']//2, 'depth': it['depth']+1}
                it['right'] = {'value': (it['value']+1)//2, 'depth': it['depth']+1}
                it['left']['parent'] = it
                it['right']['parent'] = it
                if it['prev']:
                    it['prev']['next'] = it['left']
                else:
                    self.first = it['left']
                it['left']['next'] = it['right']
                it['right']['next'] = it['next']
                if it['next']:
                    it['next']['prev'] = it['right']
                else:
                    self.last = it['right']
                it['right']['prev'] = it['left']
                it['left']['prev'] = it['prev']
                del it['value']
                return True
            it = it['next']
        return False

    def add(self,other):
        while self.reduce():
            pass
        if other is None:
            return
        l = self.as_list()
        l = [l, other.as_list()]
        self.first = {'prev':None}
        self.root, self.last = self.fill(l, 0, self.first)
        self.first = self.first['next']
        self.first['prev'] = None
        while self.reduce():
            pass

    def __str__(self):
        result = ''
        it = self.first
        while not it is None:
            result += ' ' + str(it['value']) + '@' + str(it['depth'])
            it = it['next']
        return result


def part1(i, p1=True):
    numbers = parse(i)
    x = Number(numbers[0])
    x.add(None)
    for n in numbers[1:]:
        y = Number(n)
        y.add(None)
        x.add(y)
    print(x.magnitude())


def part2(i):
    numbers = parse(i)
    M = 0
    for n1 in numbers:
        for n2 in numbers:
            if n1 == n2:
                continue
            x1 = Number(n1)
            x1.add(None)
            x2 = Number(n2)
            x2.add(None)
            x1.add(x2)
            m = x1.magnitude()
            if m > M:
                M = m
    print(M)



if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


