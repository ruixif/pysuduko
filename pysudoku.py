#!/home/ruixif/P3/bin python
# -*- coding: utf-8 -*-


             

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

#build the 9x9 square
digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)



def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for (s,d) in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False

    return values

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values

    values[s] = values[s].replace(d, '')

    #If a sqaure is reduced to one value d2, then eliminate d2 from peers
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False

    #If a unit u is reduced to only one place for a value d, then put it there
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) ==1:
            if not assign(values, dplaces[0], d):
                return False

    return values

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    return dict(zip(squares, chars))


def display(values):
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        string_tmp = ''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols)
        print(string_tmp)
        if r in 'CF':
            print(line)

def solve(grid): 
    return search(parse_grid(grid))

def search(values):
    #early death
    if values is False:
        return False
    #solved
    if all((len(values[s]) == 1) for s in squares):
        return values
    #choose the unfilled square with fewest options
    n, s = min((len(values[s]),s) for s in squares if len(values[s]) > 1 )
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def some(seq):
    for e in seq:
        if e: return e
    return False

sample_grid = \
"""
400000805
030000000
000700000
020000060
000080400
000010000
000603070
500200000
104000000"""


xxx = parse_grid(sample_grid)
display(xxx)
sss = solve(solve(sample_grid))
display(sss)



