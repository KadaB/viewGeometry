#!/usr/bin/env python3

import numpy as np
from numpy.linalg import inv 
from numpy.linalg import norm

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

def magnitude(v):
    #return np.sqrt( np.sum( v**2 ) )
    #return np.sqrt(sum([x*x for x in v ]))
    return norm(v)

def normalize(v):
    l = magnitude(v)
    return v / l if l != 0 else np.array( (0, 0, 0) )

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
    
def rotate(axis, angle):
    x, y, z = axis
    theta = angle * np.pi / 180.
    aaT = np.array([[ x*x, y*x, z*x],
                    [ x*y, y*y, z*y],
                    [ x*z, y*z, z*z]])
    A_cross = np.array([[ 0,-z, y],
                        [ z, 0,-x],
                        [-y, x, 0]])
    return np.identity(3) * np.cos(theta) + aaT *(1 - np.cos(theta) ) + A_cross * np.sin(theta)

# translation matrix 
def translate(x, y, z):
    T = np.array([[1, 0, 0, x], 
                  [0, 1, 0, y], 
                  [0, 0, 1, z],
                  [0, 0, 0, 1]])
    return T

def scale(sx, sy, sz):
    S = np.array([[sx, 0, 0, 0], 
                  [0,sy, 0, 0], 
                  [0, 0,sz, 0],
                  [0, 0, 0, 1]])
    return S

# check the output of the operation, is np.linalg.inv 
# really the inverse of combation of inverste transformations
def ot_IsInverseEqual():
    R = rotate( (0, 0, 1), 90. )
    R_inv = rotate( (0, 0, 1), -90. )
    T = translate(1, 1, 0) 
    T_inv = translate(-1, -1, 0) 
    S = scale(5, 5, 1)
    S_inv = scale(1/5, 1/5, 1)

    M = T.dot(mat4(R).dot(S))
    M_inv = S_inv.dot(mat4(R_inv).dot(T_inv))

    print(M)
    print()
    print(M_inv)
    print()
    print(inv(M))

def clampRGB(v):
    v0 = min(max(v[0], 0), 1)
    v1 = min(max(v[1], 0), 1)
    v2 = min(max(v[2], 0), 1)
    return np.array( (v0, v1, v2) )

if __name__ == '__main__':
    print("HallO");
    
