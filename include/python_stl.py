from consts import *

def GET_VALUE_TERMINAL(tup, idx):
    return tup[idx]

def GET_VALUE(tup, idx):
    return tup[idx]

def GET_WORLD(a, xy):
    return a[xy[1]][xy[0]]

def FIRST(xy):
    return xy[0]

def SECOND(xy):
    return xy[1]

def PRINT(v):
    print v

def ALLOCATE_ARRAY(x, size):
    for i in xrange(ARRAY_SIZE):
        x[i] = 0

def GET_ARRAY_VALUE(a, pos):
    return a[pos]

def SET_ARRAY_VALUE(a, pos, value):
    a[pos] = value

def LENGTH(a):
    return len(a)

# Array (for compability)
queue = [0] * ARRAY_SIZE
distance = [0] * ARRAY_SIZE
