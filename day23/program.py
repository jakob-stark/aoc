import argparse
import itertools as it
from ctypes import *

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

class Game(Structure):
    _fields_ = [ ('hallway', c_byte*7),
                 ('rooms',   c_byte*16) ]

libi = CDLL('./search.so')
libi.search.restype = c_int
    
def parse(inp, p1=True):
    if p1:
        inp.insert(4,'#A#B#C#D#')
        inp.insert(5,'#A#B#C#D#')
    else:
        inp.insert(3,'#D#C#B#A#')
        inp.insert(4,'#D#B#A#C#')
    ro = tuple((inp[k].strip('#').split('#') for k in range(2,2+4)))
    hw = inp[1].strip('#')
    hw = hw[0], hw[1], hw[3], hw[5], hw[7], hw[9], hw[10]
    game = Game()
    for p, r in it.product(range(4),range(4)):
        game.rooms[r*4+p] = {'A':0,'B':1,'C':2,'D':3,'.':-1}[ro[p][r]]
    for i in range(7):
        game.hallway[i] = {'A':0,'B':1,'C':2,'D':3,'.':-1}[hw[i]]
    return game

def part1(i,p1=True):
    game = parse(i,p1)
    result = libi.search(pointer(game), 50000, 2 if p1 else 4)
    print(result)

def part2(i):
    part1(i, p1=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


