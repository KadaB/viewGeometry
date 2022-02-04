#!/usr/bin/env python3

#glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
#glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import mathadd as npa
from camera import *

class Scene: # gathers geometry and renders
    def __init__(myList):
        pass
    def draw():
        pass
    def intersect():
        pass

class Geometry:
    def __init__(self):
        self.solidColor = (0.5, 0.5, 0.5, 1)
        self.wireColor = (0, 0, 0, 1)
    def draw(self, wire=False):
        pass
    def intersect(o, d):
        pass

class Circle(Geometry):
    def draw(self, wire=False):
        glColor(self.wireColor)
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_SILHOUETTE)
        gluDisk(quadric, 0, .5, 20, 1)

# a cross looking in plane direction
class CrossPlane(Geometry):
    def __init__(self):
        pass
    def draw(self):
        pass
        # n und seine Länge?
        # oder a und b

class Disk(Geometry):
    def draw(self, wire=False):
        glColor(self.solidColor)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0, .5, 20, 1)

class Sphere(Geometry):
    def __init__(self):
        self.center = (0, 0, 0)
        self.solidColor = (0.6, 0.6, 0.6, 0.5)

    def draw(self,wire=False):
        glPushMatrix()
        glTranslate(*self.center)
        if wire:
            damp = 0.6
            color=self.solidColor
            glColor(color[0] * damp, color[1] * damp, color[2] * damp, 1) 
            quadric = gluNewQuadric()
            #gluQuadricDrawStyle(quadric, GLU_LINE)
            gluQuadricDrawStyle(quadric, GLU_SILHOUETTE)
            gluSphere(quadric, 0.5, 10, 10)
        else:
            glColor(*self.color)
            quadric = gluNewQuadric()
            gluSphere(quadric, 0.5, 10, 10)

        glPopMatrix()

    def intersect(o, d):
        pass

class Vector:
    def __init__(self, o, d, text, textShift=(0, 0, 0), orthUp=(0, 1, 0)):
        self.o = o
        self.d = d
        self.text = text
        self.textShift = textShift
        self.orthUp = orthUp
        self.solidColor = (0, 0, 0.7, 1)
    def draw(self):
        end = self.o+self.d
        Arrow(self.o, self.d, color = self.solidColor).draw()
        Point(self.o, color = self.solidColor).draw()
        #Point(end).draw()

        xShift, yShift, zShift = orthogonalizeFromDir(-self.d, self.orthUp) # rhc
        shifts = self.textShift[0] * xShift + self.textShift[1] *  yShift + self.textShift[2] * zShift
        Text(np.add(end, shifts), self.text).draw()

class Cube(Geometry):
    def __init__(self, size = 1):
        self.pos = (0, 0, 0)
        s = size / 2
        vertices = [(-s, s, s), (-s,-s, s), ( s,-s, s), ( s, s, s), # front
                    ( s, s,-s), (-s, s,-s), (-s,-s,-s), ( s,-s,-s), # back
                    (s, -s, s), (s, -s,-s), (s,  s,-s), (s,  s, s), # right
                    (-s, s, s), (-s,-s, s), (-s,-s,-s), (-s, s,-s), # left
                    (-s, s, s), (-s, s,-s), ( s, s,-s), ( s, s, s), # top
                    (-s, -s, s), (-s, -s,-s), ( s, -s,-s), ( s, -s, s)] # bottom
    def draw(self,wire=False):
        glPushMatrix()
        glTranslate(*self.pos)

        if wire:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        glBegin(GL_QUADS)
        for v in vertices:
            glVertex(*v)
        glEnd()

        glPopMatrix()

        if wire:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

class Cone(Geometry):
    def __init__(self, radius, length):
        self.r = radius
        self.l = length
    def draw(self,wire=False):
        gluCylinder(gluNewQuadric(), self.r, 0, self.l, 5, 5);

class Cylinder(Geometry):
    def __init__(self, radius, length):
        self.r = radius
        self.l = length
    def draw(self,wire=False):
        gluCylinder(gluNewQuadric(), self.r, self.r, self.l, 5, 5);

class Triangle(Geometry):
    def __init__(self, A, B, C, color=(1, 0.3, 0.3, 0.5)):
        self.A, self.B, self.C = A, B, C
        self.color = color
    def draw(self,wire=False):
        color = self.color
        if wire:
            color = (color[0], color[1], color[2], 1)
        glColor(*color)
        glBegin(GL_LINE_LOOP if wire else GL_TRIANGLES)
        glVertex(*self.A)
        glVertex(*self.B)
        glVertex(*self.C)
        glEnd()

class Point(Geometry):
    def __init__(self, pos, color=(0.3, 0.3, 0.3, 1)):
        self.pos = pos
        self.color = color
        self.res = 10
        self.size = 0.07 # diameter

    def draw(self,wire=False):
        glPushMatrix()
        glTranslate(*self.pos)
        glColor(*self.color)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.size/2, self.res, self.res)
        glPopMatrix()

class LineSection(Geometry):
    def __init__(self, startPos, endPos, lineWidth = 0.0, epsilon = 0.001):
        self.startPos = startPos
        self.endPos = endPos
        self.lineWidth = lineWidth
        self.epsilon = epsilon

    def draw(self,wire=False):
        #glColor(0, 0, 0, 1)

        if wire or (self.lineWidth < self.epsilon):
            glBegin(GL_LINES)
            glVertex(self.startPos)
            glVertex(self.endPos)
            glEnd()
        else:
            glPushMatrix()
            dir_vec = np.subtract(self.endPos, self.startPos)
            M = getOrientTowardsMatrix(self.startPos, *orthogonalizeFromDir(dir_vec))
            glMultMatrixf(M.transpose())
            r = self.lineWidth / 2
            length = npa.norm(dir_vec)

            gluCylinder(gluNewQuadric(), r, r, length, 5, 5);
            glPopMatrix()
    
class Arrow(Geometry):
    def __init__(self, startPos, vectorDirection, color=(1, 0, 0, 1), linewidth=0): #0.02
        pass
        self.headLength = 0.2
        self.headWidth = 0.05
        self.set_back = True    # include arrow head in overall length
        self.startPos = startPos
        self.dir_vec = vectorDirection
        self.linewidth=linewidth
        self.solidColor = color

    def draw(self,wire=False):
        linelen = npa.norm(self.dir_vec)
        direction = npa.normalize(self.dir_vec)

        if self.set_back or linelen < self.headLength:
            linelen -= self.headLength

        endPos = self.startPos + linelen * direction

        # draw arrow head
        glPushMatrix()
        glColor(*self.solidColor)
        M = getOrientTowardsMatrix(endPos, *orthogonalizeFromDir(self.dir_vec))
        glMultMatrixf(M.transpose())
        gluCylinder(gluNewQuadric(), self.headWidth, 0, self.headLength, 5, 5);
        glPopMatrix()

        # arrow shaft
        LineSection(self.startPos, endPos, self.linewidth).draw(wire)

class Text(Geometry):
    def __init__(self, pos, text):
        self.text = text
        self.pos = pos

    def draw(self,wire=False):
        glRasterPos(*self.pos)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, self.text)

class Origin(Geometry):
    def __init__(self, linewidth=0):
        self.linewidth = linewidth
        pass
    def draw(self,wire=False):
        glPushMatrix()
        glDisable(GL_DEPTH_TEST)

        glColor(1, 0, 0)
        glRasterPos(1, 0, 0)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'x')

        glColor(0, 1, 0)
        glRasterPos(0, 1, 0)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'y')

        glColor(0, 0, 1)
        glRasterPos(0, 0, 1)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, b'z')
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()

        x, y, z = np.eye(3)
        Arrow((0, 0, 0), x, x, self.linewidth).draw()#, (1, 0, 0, 1))
        Arrow((0, 0, 0), y, y, self.linewidth).draw()#, (0, 1, 0, 1))
        Arrow((0, 0, 0), z, z, self.linewidth).draw()#, (0, 0, 1, 1))

# damit man start, end angeben kann, statt start, start + richtung
class ArrowLineSection(Geometry):
    def __init__(self):
        pass
    def draw(self,wire=False):
        pass

class Plane(Geometry):
    def __init__(self, c, a, b, color = (.8, .8, .6, 0.5)):
        self.a, self.b, self.c = a, b, c
        self.solidColor = color

    def draw(self,wire=False):
#        if wire:
#            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
        glColor(*self.solidColor)
        
        a, b, c = self.a, self.b, self.c

        A = c - a + b
        B = c - a - b
        C = c + a - b
        D = c + a + b

        glBegin(GL_QUADS)
        glVertex(*A)
        glVertex(*B)
        glVertex(*C)
        glVertex(*D)
        glEnd()

        glColor(.6, .6, .4, 1)
        glBegin(GL_LINE_LOOP)
        glVertex(*A)
        glVertex(*B)
        glVertex(*C)
        glVertex(*D)
        glEnd()
#        if wire:
#            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

class GridPlane(Geometry):
    def __init__(self, size=5):
        self.size = size
    def draw(self,wire=False):
        size = self.size
        if True:
            glColor(.8, .8, .6);
            glBegin(GL_LINES)
            steps = self.size*2+1
            for i in np.linspace(-size, size, steps):
                glVertex(i, 0, size)
                glVertex(i, 0, -size);
                glVertex(size, 0, i)
                glVertex(-size, 0, i);
            glEnd()
        #else:
            glColor(.9, .9, .7, .5);
            glBegin(GL_QUADS)
            glVertex(-size, 0, -size)
            glVertex(-size, 0, size)
            glVertex(size, 0, size)
            glVertex(size, 0, -size)
            glEnd()
