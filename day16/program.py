import argparse
import functools as ft
import operator as op
import re
#import numpy as np
#import scipy as sp
#import scipy.ndimage as si
#import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return ''.join(map(lambda h: bin(int(h,16)+16)[3:], i[0]))

def parse_packets(bs):
    pos = 0
    task = 'header'
    opl = []

    try:
        while True:
            if task == 'header':
                pv = int(bs[pos:pos+3],2) ; pos += 3
                pt = int(bs[pos:pos+3],2) ; pos += 3
                _ = bs[pos+3]
                if pt == 4:
                    task = 'literal'
                else:
                    task = 'oplen'
                yield ('pv', pv)
                yield ('pt', pt)
            if task == 'literal':
                more = True
                value = 0
                while more:
                    more = bool(int(bs[pos:pos+1],2))            ; pos += 1
                    value = value * 0x10 + int(bs[pos:pos+4],2) ; pos += 4
                task = 'header'
                yield ('lt', value)

                while len(opl) > 0:
                    lt, num = opl.pop()
                    if lt:
                        if num - 1 > 0:
                            opl.append((lt, num-1))
                            break
                        else:
                            yield ('oe', None)
                    else:
                        if pos < num:
                            opl.append((lt, num))
                            break
                        else:
                            yield ('oe', None)
            if task == 'oplen':
                lt = bool(int(bs[pos:pos+1],2))                  ; pos += 1
                if lt:
                    num = int(bs[pos:pos+11],2)                  ; pos += 11
                else:
                    num = int(bs[pos:pos+15],2) + pos + 15       ; pos += 15
                opl.append((lt, num))
                task = 'header'
                yield ('os', None)
    except:
        pass

def part1(i):
    bs = parse(i)
    #print(list(parse_packets(bs)))
    print(sum(filter(lambda x: not x is None, map(lambda x: x[1] if x[0] == 'pv' else None,
        parse_packets(bs)
    ))))

def part2(i):
    bs = parse(i)

    def token_to_string(token):
        key, val = token
        if key == 'os':
            return '('
        if key == 'oe':
            return '),'
        if key == 'pt':
            return {0: 'xsum', 1:'xmul', 2:'xmin', 3:'xmax', 5:'xgt', 6:'xlt', 7:'xeq'}.get(val,'')
        if key == 'lt':
            return str(val) + ','
        return ''

    def xsum(*a):
        return ft.reduce(op.add, a)

    def xmul(*a):
        return ft.reduce(op.mul, a)

    def xmin(*a):
        return min(a)

    def xmax(*a):
        return max(a)
    
    def xgt(a,b):
        return int(a>b)

    def xlt(a,b):
        return int(a<b)

    def xeq(a,b):
        return int(a==b)

    expr = ''.join(map(token_to_string, parse_packets(bs)))

    expr = re.sub(',\)',')', expr)[:-1]
    #print(expr)
    print(eval(expr))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


