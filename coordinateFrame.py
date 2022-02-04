#!/usr/bin/env python3
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import mathadd as npa
from geometries import *
from camera import *

def myInit():
    glClearColor(1.0, 1.0, 1.0, 0.0) 

    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glClearDepth(GL_TRUE)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable( GL_BLEND )

    glDisable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    pos = (.5, 2, 5)
    target = (0, 0, 0)
    up = (0, 1, 0)

    V = cam.getCamMatrix()
    glLoadMatrixd(V.transpose())

    def drawScene(wire=False):
        Origin().draw()

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
            Point(-w).draw()

            #GridPlane(5).draw()

        cameraFrame(5, 4, 45)
        GridPlane().draw(True)
        

    def processScene():
        glEnable(GL_BLEND)
        drawScene()

    processScene()

    glFlush()
    glutSwapBuffers()

def resize(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    glViewport(0, 0, w, h)
    fovy = 45
    zNear = 0.1
    zFar = 100
    aspect = w / h

    gluPerspective(fovy, aspect, zNear, zFar)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def on_key(keycode, x, y):
    global rotationAngle

    if keycode == b'q':
        glutLeaveMainLoop()
    elif keycode == b'k':
        cam.pitchSpin(np.pi/10)
    elif keycode == b'i':
        cam.pitchSpin(-np.pi/10)
    elif keycode == b'l':
        cam.yawSpin(np.pi/10)
    elif keycode == b'j':
        cam.yawSpin(-np.pi/10)
    elif keycode == b'p':
        cam.move(-0.5)
    elif keycode == b'\xc3':
        cam.move(0.5)
    elif keycode == b'\r':
        print("cam pos:", cam.pos)
    else:
        rotationAngle = (rotationAngle + 10) % 360

    if False:
        print('keycode pressed:', keycode)

    glutPostRedisplay()

rotationAngle = 0

cam = CrystalBallCamera()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_STENCIL)   
glutInitWindowSize(640, 480)  
glutInitWindowPosition(100, 100)  
glutCreateWindow("My OpenGL Code")
glutReshapeFunc(resize)
glutKeyboardFunc(on_key)
myInit()
glutDisplayFunc(display) 
glutMainLoop()
