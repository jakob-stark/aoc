import itertools as it

input_filename = "star1.input"
#input_filename = "star1.example"

def pairwise(iterable):
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a,b)

if __name__ == "__main__":
    with open(input_filename) as f:
        print( sum( it.starmap( lambda n1, n2: n1<n2, pairwise(map(int,f)))))
