#!/usr/bin/env python3

import numpy as np
from numpy.linalg import inv 
from numpy.linalg import norm

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

def normalize(v):
    l = norm(v)
    return np.divide(v, l) if l != 0 else np.array( (0, 0, 0) )

def homogenize(v, w = 1):       # vector: w = 0, point: w = 1
    return np.append(v, w)

def dehomogenize(v, w = 1):     # vector: w = 0, point: w = 1
    W = v[-1] if w != 0 else 1
    return np.divide(v[:-1], W )

# takes row vector and outputs column vector
def colVector(v):
    if len(np.shape(v)) > 1:
        raise ValueError('Only column vectors of dim (d,) allowed: ' + str(np.shape(v)) + ' given.') 
    return np.array( [ [x] for x in v ] )

# takes col vector and outputs row vector
def rowVector(v):
    shape = np.shape(v)
    if len(shape) == 2 and shape[1] == 1:
        return np.array( [ y for x in v for y in x ] )
    else:
        raise ValueError('No row vector: ' + str(np.shape(v)) + ' given.') 

def mat4(M):
    dim = np.shape(M)
    if len(dim) == 2 and dim[0] == dim[1] and dim[0]== 3:
        N = [ np.append(row, 0) for row in M ]
        N += [ [0, 0, 0, 1] ]
        return np.array(N)
    else:
        raise ValueError('Only Mat3 allowed: {} given.'.format(dim)) 

def mat3(M):
    dim = np.shape(M)
    if len(dim) == 2 and dim[0] == dim[1] and dim[0] >= 4:
        N = [ row[:3] for row in M[:3] ]
        return np.array(N)
    else:
        raise ValueError('Only Mat4 allowed: {} given.'.format(dim)) 
    return np.reshape(M, (3, 3))
