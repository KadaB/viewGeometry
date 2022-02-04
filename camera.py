#!/usr/bin/env python3
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import mathadd as npa
from geometries import *

# angle axis rotation
def rotate(n, theta):
    P = np.column_stack( [ np.multiply(np.dot(n, e), n) for e in np.eye(3) ] ) 
    K = np.column_stack( [ np.cross(n, e) for e in np.eye(3) ] )
    return P + np.cos(theta) * (np.eye(3) - P) + np.sin(theta) * K

def orthogonalizeFromDir(lookDir, worldUp=(0, 1, 0), worldForward=(0, 0, -1)):
    z = npa.normalize( lookDir ) 

    if z[0] == 0 and z[2] == 0: # x and z components of z-vec are 0, shows straight up
        if z[1] > 0:
            worldUp = worldForward
        else:
            worldUp = np.multiply(worldForward, -1)

    x = npa.normalize( np.cross(worldUp, z) )
    y = npa.normalize( np.cross(z, x) )
    return x, y, z

def getOrientTowardsMatrix(pos, x, y, z):
    e1, e2, e3, _ = np.eye(4)
    R = npa.mat4(np.column_stack( [ x, y, z ] ))
    T = np.column_stack( [ e1, e2, e3, (pos[0], pos[1], pos[2], 1)])
    return T.dot(R)

class CrystalBallCamera:
    def __init__(self, pos = (3, 3, 6), target=(0, 0, 0), worldUp=(0, 1, 0)):
        self.target = target
        self.pos = pos
        lookDir = np.subtract(target, pos)
        self.x, self.y, self.z = orthogonalizeFromDir(lookDir * -1) # rhc camera z
    
    def pitchSpin(self, theta, worldUp=(0, 1, 0)):    # hoch/runter, nicken, rotationsachse ist x-achse
        R = rotate(self.x, theta)

        direction = np.subtract(self.pos, self.target)         # negative z for RHCSystem, and vektor from target to point
        new_dir = R.dot( direction )
        self.z = npa.normalize( new_dir )
        self.y = npa.normalize( R.dot( self.y ) )
        # x stays the same (axis of rotation
        self.pos = np.add(self.target, new_dir)

    def yawSpin(self, theta, worldUp=(0, 1, 0)):      # links/recht, gieren, rotationsachse ist y-achse
        # hier muss man nur um world up rotieren...
        R = rotate(worldUp, theta)
        direction = np.subtract(self.pos, self.target)         # negative z for RHCSystem, and vektor from target to point

        new_dir = R.dot( direction )
        self.z = npa.normalize( new_dir )
        self.x = npa.normalize( R.dot(self.x) )
        self.y = npa.normalize( R.dot(self.y) )
        # y muss diesmal angepasst werden, weil sie an worldUp rotatiert wird.
        self.pos = np.add(self.target, new_dir)
    
    def move(self, units):
        self.pos += self.z * units
    
    def getCamMatrix(self):
        return npa.inv(getOrientTowardsMatrix(self.pos, self.x, self.y, self.z))
