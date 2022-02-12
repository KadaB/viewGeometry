#!/usr/bin/env python3
from basic3d import *

def drawScene():
    GridPlane().draw(True)
    Origin().draw()

    O = np.array( [0, 0, 0] )
    D = np.array( [2, 2, 2] )
    V = np.array( [1.5, 2, 1] )
    P = (np.dot(V, D) * D) / npa.norm(D)**2
    R = V - P
    W = np.cross(D / npa.norm(D), R)

    Vector(O, D, b"D").draw()
    Vector(O, V, b"V").draw()
    Vector(O, P, b"P").draw()
    Vector(P, R, b"R", (-.05, .05, .1), D).draw()
    Vector(P, W, b"W").draw()
    Plane(P, R, W).draw()

    # circle on plane of rotation
    with DrawContext([getOrientTowardsMatrix(P, *orthogonalizeFromDir(D))]):
        l = npa.norm(R) * 2
        glScale(l, l, 1)
        glColor(1, 0, 0, .5)
        Circle().draw()

if __name__ == '__main__':
    glut = MyGlut(mydisplay=drawScene)
    glut.run()