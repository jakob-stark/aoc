import argparse as ap
import numpy as np
import functools as ft
import operator as op
import itertools as it

def read(f):
        return map(str.strip, f)

class Board:
    def __init__(self, t):
        self.field = np.array(t)
        self.marked = np.zeros(self.field.shape, dtype=int)

    def has_won(self):
        for r in range(5):
            if np.sum(self.marked[:,r]) == 5:
                return True
            if np.sum(self.marked[r,:]) == 5:
                return True
        return False
    
    def sum_of_unmarked(self):
        return np.sum(self.field[self.marked == 0])

    def mark(self, n):
        self.marked[self.field == n] = 1

    def __str__(self):
        return str(self.field) + '\n' + str(self.marked)


def parse(i):
    yield tuple(map(int,str.split(next(i),',')))
    board = []
    for l in i:
        if l != '':
            board.append(tuple(map(int,str.split(l))))
        if len(board) >= 5:
            yield Board(board)
            board = []

def part1(i):
    boards = list(parse(i))
    numbers = boards.pop(0)
    for n in numbers:
        for b in boards:
            b.mark(n)
            if b.has_won():
                print(b.sum_of_unmarked() * n)
                return

def part2(i):
    boards = list(parse(i))
    numbers = boards.pop(0)
    for n in numbers:
        for b in boards:
            b.mark(n)
        if len(boards) == 1 and boards[0].has_won():
            print(boards[0].sum_of_unmarked() * n)
            return
        boards = list(filter(lambda b: not b.has_won(), boards))


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

