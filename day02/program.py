import itertools as it
import functools as ft
import operator as op

def parse(f):
    return it.starmap( lambda k,v : (k, int(v)),
        map(str.split,
            map(str.strip,
                f
            )
        )
    )

def part1():
    with open('input') as f:
        print(
            ft.reduce( op.mul ,
                ft.reduce( lambda vec1, vec2 : map(op.add, vec1, vec2),
                    it.starmap( lambda k, v : {'forward':(v,0),'down':(0,v),'up':(0,-v)}[k], 
                        parse(f)
                    )
                )
            )
        )

def part2():
    with open('input') as f:
        print(
            (lambda s : s[0]*s[2])(
                ft.reduce( lambda s, e : (s[0]+e[0], s[1]+e[1], s[2]+e[0]*s[1]),
                    it.starmap( lambda k, v : {'forward':(v,0,0),'down':(0,v,0),'up':(0,-v,0)}[k], 
                        parse(f)
                    )
                )
            )
        )

part2()

