import argparse
import numpy as np

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(i):
    return map(int,i[0].split(','))

def part1(i,N):
    fish,_ = np.histogram(list(parse(i)), bins=range(11))
    for i in range(N):
        fish[7] += fish[0]
        fish[9] += fish[0]
        fish[0] = 0
        fish = np.roll(fish,-1)
        with np.printoptions(formatter={'int':lambda x : '{:3}'.format(x)}):
            #print(fish, np.sum(fish))
            pass
    print(np.sum(fish))

def part1t(i,N):
    b,_ = np.histogram(list(parse(i)), bins=range(10))
    M = np.array(((0,1,0,0,0,0,0,0,0),
                  (0,0,1,0,0,0,0,0,0),
                  (0,0,0,1,0,0,0,0,0),
                  (0,0,0,0,1,0,0,0,0),
                  (0,0,0,0,0,1,0,0,0),
                  (0,0,0,0,0,0,1,0,0),
                  (1,0,0,0,0,0,0,1,0),
                  (0,0,0,0,0,0,0,0,1),
                  (1,0,0,0,0,0,0,0,0)))
    print(np.sum(np.einsum('ij,j->i',np.linalg.matrix_power(M,N),b)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')
    parser.add_argument('-t', action='store_true', help='use theoretical formula')

    args = parser.parse_args()

    if args.p == 1:
        if args.t:
            part1t(read(args.i),80)
        else:
            part1(read(args.i),80)
    elif args.p == 2:
        if args.t:
            part1t(read(args.i),256)
        else:
            part1(read(args.i),256)



