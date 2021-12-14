import argparse
#import numpy as np
#import scipy as sp
#import scipy.ndimage as si
#import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    template = list(i[0])
    rules = dict(map(lambda l: l.split(' -> '), i[2:]))
    return template, rules


def part1(i):
    template, rules = parse(i)

    def grow():
        pos = 1
        for pair in zip(template[:-1],template[1:]):
            template.insert(pos, rules[''.join(pair)])
            pos += 2

    for i in range(10):
        grow()

    counts = {l: template.count(l) for l in set(template)}
    print(max(counts.values())-min(counts.values()))


def part2(i):
    template, rules = parse(i)
    elements = set(rules.values()) | set(template)
    hashmap = {}

    def count(string, step, inclusive=True):
        # try to find the branch in the hashmap
        result = hashmap.get((string,step,inclusive), None)
        if result:
            return result

        # if we reached the bottom, just count the characters
        # the inclusive flag tells us if the last character is counted
        # or not
        if step == 0:
            if not inclusive:
                return {l: string[:-1].count(l) for l in elements}
            else:
                return {l: string[:].count(l) for l in elements}

        # recurse for each pair
        result = {l:0 for l in elements}
        for i, pair in enumerate(zip(string[:-1],string[1:])):
            lhs = count(pair[0]+rules[''.join(pair)], step-1, False)
            rhs = count(rules[''.join(pair)]+pair[1], step-1,
                                   inclusive and i+2 == len(string))
            result = {l: result[l] + lhs[l] + rhs[l] for l in elements}

        # store the result in the hashmap and return it
        hashmap[(string,step,inclusive)] = result
        return result

    result = count(''.join(template), 40)
    print(max(result.values())-min(result.values()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


