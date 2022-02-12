# viewGeometry
A simple geometry viewer to display vector math.

It's still based on GLUT and legacy OpenGL and has rudimentary camera control with

    i = rotate camera up
    j = rotate camera left
    k = rotate camera down
    l = rotate camera right
    p = zoom in
    ; = zoom out (ö german)

![image](https://github.com/KadaB/viewGeometry/blob/main/image.png)

## example
Example to display a plane


    from basic3d import *
    
    def drawScene(wire=False):
        Plane((0, 1.5, 1), (1, 0, 0), (0, 1, 0)).draw()
    
    glut = MyGlut(mydisplay=drawScene)
    glut.run()


## run
i.e.:

    python axis_angle.py

## Dependencies
- python3

Install with pip3
- numpy
- OpenGL.GL
- OpenGL.GLUT
- OpenGL.GLU

