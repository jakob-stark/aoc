import argparse
import itertools as it

def read(fn):
    with open(fn) as f:
        return list(map(str.strip, f))

def parse(inp):
    return list(map(lambda t: t.split(), inp))

def run(instr, inpt):
    inpt = iter(inpt)

    reg = {r:0 for r in 'wxzy'}
    for i in instr:
        if not i:
            continue
        if i[0] == 'inp':
            reg[i[1]] = int(next(inpt))
        if i[0] == 'add':
            reg[i[1]] = reg[i[1]] +  (reg[i[2]] if i[2] in 'wxzy' else int(i[2]))
        if i[0] == 'mul':
            reg[i[1]] = reg[i[1]] *  (reg[i[2]] if i[2] in 'wxzy' else int(i[2]))
        if i[0] == 'div':
            reg[i[1]] = reg[i[1]] // (reg[i[2]] if i[2] in 'wxzy' else int(i[2]))
        if i[0] == 'mod':
            reg[i[1]] = reg[i[1]] %  (reg[i[2]] if i[2] in 'wxzy' else int(i[2]))
        if i[0] == 'eql':
            reg[i[1]] = int(reg[i[1]] == (reg[i[2]] if i[2] in 'wxzy' else int(i[2])))

    return reg

def part1(i,p1=True):
    instr = parse(i)

    stack = []
    solution = [0]*14
    for k in range(14):
        cmp, val = int(instr[k*18+5][2]), int(instr[k*18+15][2])
        if cmp < 0:
            cmp = -cmp
            ok, ocmp, oval = stack.pop()
            #print('w{} + {} == w{} + {}'.format(ok, oval, k, cmp))
            solution[ok] = min(9, 9 - (oval-cmp))
            solution[ k] = min(9, 9 - (cmp-oval))
        else:
            stack.append((k,cmp,val))
    solution = ''.join(map(str,solution))

    #print(run(instr, solution))
    print(solution)

def part2(i):
    instr = parse(i)

    stack = []
    solution = [0]*14
    for k in range(14):
        cmp, val = int(instr[k*18+5][2]), int(instr[k*18+15][2])
        if cmp < 0:
            cmp = -cmp
            ok, ocmp, oval = stack.pop()
            #print('w{} + {} == w{} + {}'.format(ok, oval, k, cmp))
            solution[ok] = max(1, 1 - (oval-cmp))
            solution[ k] = max(1, 1 - (cmp-oval))
        else:
            stack.append((k,cmp,val))
    solution = ''.join(map(str,solution))

    #print(run(instr, solution))
    print(solution)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('-p', type=int, choices=(1,2), help='part')
    parser.add_argument('-i', type=str, help='input file')

    args = parser.parse_args()

    if args.p == 1:
        part1(read(args.i))
    elif args.p == 2:
        part2(read(args.i))


