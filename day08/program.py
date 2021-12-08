import argparse
import numpy as np
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return list(map(lambda e : tuple(map(str.split,e.split(' | '))), i))

def part1(i):
    L = parse(i)
    count = np.zeros((10,),dtype=int)
    for k, o in L:
        c,_ = np.histogram(
                list(
                    filter( lambda x : not x is None,
                        map( lambda x : {2:1,3:7,4:4,7:8}.get(len(x), None),
                            o
                        )
                    )
                ),
                bins=range(11)
        )
        count = count + c
    print(np.sum(count))


def part2(i):
    ref_words = {frozenset('abcefg' ) :'0',
                 frozenset('cf'     ) :'1',
                 frozenset('acdeg'  ) :'2',
                 frozenset('acdfg'  ) :'3',
                 frozenset('bdcf'   ) :'4',
                 frozenset('abdfg'  ) :'5',
                 frozenset('abdefg' ) :'6',
                 frozenset('acf'    ) :'7',
                 frozenset('abcdefg') :'8',
                 frozenset('abcdfg' ) :'9'}

    def revert(words):
        ref_s = ''.join(map(''.join,filter(lambda w: len(w) < 7, ref_words)))
        ref_t = ''.join(map(''.join,filter(lambda w: len(w) < 6, ref_words)))
        ref_dict = {(ref_s.count(c), ref_t.count(c)) : c for c in 'abcdefg'}

        s = ''.join(filter(lambda w: len(w) < 7,words))
        t = ''.join(filter(lambda w: len(w) < 6,words))

        return {c: ref_dict[(s.count(c), t.count(c))] for c in 'abcdefg'}

    L = parse(i)
    s = 0
    for words, digits in L:
        t = str.maketrans(revert(words))
        s += int(''.join(map(lambda d: ref_words[frozenset(d.translate(t))], digits)))
    print(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


