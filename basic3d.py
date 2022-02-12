#!/usr/bin/env python3
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import numpyadd as npa
from geometries import *
from camera import *

class MyGlut:
    def __init__(self, res = (640, 480), mydisplay=None, mykey=None, title="basic 3d"):
        self.rotationAngle = 0

        self.cam = CrystalBallCamera()
        self.w, self.h = res
        self.title = title

        self.mydisplay = mydisplay
        self.mykey = mykey

        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_STENCIL)   
        glutInitWindowSize(self.w, self.h)  
        glutInitWindowPosition(100, 100)  
    
    def run(self):
        glutCreateWindow(self.title)
        glutReshapeFunc(self.resize)
        glutKeyboardFunc(self.on_key)
        glutDisplayFunc(self.display) 
        self.myInit()
        glutMainLoop()

    def myInit(self):
        glClearColor(1.0, 1.0, 1.0, 0.0) 

        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glClearDepth(GL_TRUE)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable( GL_BLEND )

        glDisable(GL_CULL_FACE)
        glDisable(GL_LIGHTING)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        with DrawContext([self.cam.getCamMatrix()]):
            GridPlane().draw(True)
            Origin().draw()

            try:
                self.mydisplay()
            except:
                pass

        glFlush()
        glutSwapBuffers()

    def resize(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        self.w, self.h = w, h

        glViewport(0, 0, w, h)
        fovy = 45
        zNear = 0.1
        zFar = 100
        aspect = w / h

        gluPerspective(fovy, aspect, zNear, zFar)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_key(self, keycode, x, y):
        if keycode == b'q':
            glutLeaveMainLoop()
        elif keycode == b'k':
            self.cam.pitchSpin(np.pi/10)
        elif keycode == b'i':
            self.cam.pitchSpin(-np.pi/10)
        elif keycode == b'l':
            self.cam.yawSpin(np.pi/10)
        elif keycode == b'j':
            self.cam.yawSpin(-np.pi/10)
        elif keycode == b'p':
            self.cam.move(-0.5)
        elif keycode == b'\xc3':
            self.cam.move(0.5)
        elif keycode == b'\r':
            print("cam pos:", self.cam.pos)
        else:
            #self.rotationAngle = (self.rotationAngle + 10) % 360
            try:
                self.mykey(keycode, x, y)
            except:
                pass

        if False:
            print('keycode pressed:', keycode)

        glutPostRedisplay()


if __name__=='__main__':
    def draw():
        Point((0, 0, 0)).draw()

    glut = MyGlut(mydisplay=draw)
    glut.run()
