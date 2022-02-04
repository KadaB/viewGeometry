#!/usr/bin/env python3
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import numpyadd as npa
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
        Plane(P, -R, W).draw()
    
        glPushMatrix()
        M = getOrientTowardsMatrix(P, *orthogonalizeFromDir(D))
        glMultMatrixf(M.transpose())
        l = npa.norm(R) * 2
        glScale(l, l, 1)
        glColor(1, 0, 0, .5)
        Circle().draw()
        glPopMatrix()

    def processScene():
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
