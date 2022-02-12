# viewGeometry
A simple geometry viewer to display vector math. So in case you are working with some vector arithmetic and you quickly want to check out if it does what you want you can write a small script displaying the vectors and planes for you.

It's still based on GLUT and legacy OpenGL and has an orbital camera control revolving around the origin with

    i = rotate camera up
    j = rotate camera left
    k = rotate camera down
    l = rotate camera right
    p = zoom in
    ; = zoom out (ö german)
    
    q = quits the program

![image](https://github.com/KadaB/viewGeometry/blob/main/image.png)

## example
Example to display a plane


    from basic3d import *
    
    def drawScene():
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

