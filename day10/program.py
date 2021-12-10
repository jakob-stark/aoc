import argparse
import numpy as np
import scipy as sp
import scipy.ndimage as si
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def part1(i):
    score = 0
    for l, line in enumerate(i):
        stack = []
        for char in line:
            if char in '([{<':
                stack.append(char)
            elif char in ')]}>':
                expect = {'(':')','[':']','{':'}','<':'>'}.get(stack.pop(), None)
                if expect != char:
                    #print('Line {}: Expected {}, but found {} instead'.format(l,expect,char))
                    score += {')':3,']':57,'}':1197,'>':25137}[char]
                    break
    print(score)


def part2(i):
    scores = []
    for l, line in enumerate(i):
        stack = []
        error = False
        for char in line:
            if char in '([{<':
                stack.append(char)
            elif char in ')]}>':
                expect = {'(':')','[':']','{':'}','<':'>'}.get(stack.pop(), None)
                if expect != char:
                    error = True
                    break
        if not error and len(stack) > 0:
            lscore = 0
            while len(stack):
                closing = {'(':')','[':']','{':'}','<':'>'}.get(stack.pop(), None)
                lscore *= 5
                lscore += {')':1,']':2,'}':3,'>':4}[closing]
            scores.append(lscore)
    print(np.median(np.array(scores,dtype=int)).astype(int))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


