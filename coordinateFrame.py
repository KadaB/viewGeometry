#!/usr/bin/env python3
from basic3d import *

def drawScene(wire=False):
    def cameraFrame(W, H, fovy, O = np.array([0, 0, 0])):
        halfW = W / 2.
        halfH = H / 2.

        aspect = W / H

        tany = np.tan(fovy * np.pi / 360) # convert to radians, but also have the fovy
        tanx = tany * aspect

        target = (0, 0, -5)
        lookDir = np.subtract(target, O)
        u, v, w = orthogonalizeFromDir(-lookDir)

        def getRayFor(j, i):
            x, y = j +.5, i +.5
            a = (x - halfW) / halfW
            b = (halfH - y) / halfH
            a *= tanx
            b *= tany

            OP = a * u + b * v - w # -w, weil nach vorne von O, also in neg richtung
            return OP 

        for i in range(H):
            for j in range(W):
                OP = getRayFor(j, i)
                P = O + OP
                arrow = Arrow(O, OP, color = (0., 0., 0.3, 1)).draw()
                #LineSection(O, P).draw()
                #Point(P).draw()
        Plane(-w, u*tanx, v*tany, (0.7, 0.4, 0.7, .5)).draw()

    cameraFrame(5, 4, 45)

if __name__ == '__main__':
    glut = MyGlut(mydisplay=drawScene)
    glut.run()