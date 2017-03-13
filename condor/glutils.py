''' Thicker wrapper around Python OpenGL bindings '''
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from condor.style import *

from math import pi, sin, cos

# TODO - move to style.py and make configurable
detail = 40
style = None

def init_window(title, width, height):
    ''' Creates window with title and width, height '''
    if {type(width), type(height)} != {int}:
        raise TypeError('init_window() width and height must be integers')

    if width <= 0 or height <= 0:
        raise ValueError('init_window() width and height must be positive')

    if type(title) is not str:
        raise TypeError('init_window() title argument must be string')

    # TODO - Variable display modes
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(bytes(title, 'utf-8'))

def set_style(new_style):
    global style
    style = new_style

def callback(loop):
    glutDisplayFunc(loop)
    glutIdleFunc(loop)
    glutMainLoop()

def prepare_2d(width, height):
    ''' Prepares for 2d rendering '''
    if {type(width), type(height)} != {int}:
        raise TypeError('prepare_2d() arguments must be integers')

    if width <= 0 or height <= 0:
        raise ValueError('prepare_2d() arguments must be positive')

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)

def clear_color(color):
    glClearColor(*color, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def rect_mode_convert(x, y, w, h):
    if style.rect_mode == CORNERS:
        if w <= x or h <= y:
            raise ValueError('For rect_mode CORNERS, first point must be' +
                'below and left of second point.')
        w -= x
        h -= x
    elif style.rect_mode == CENTER:
        x -= w/2
        y -= h/2
    elif style.rect_mode == RADIUS:
        x -= w
        y -= h
        w *= 2
        h *= 2
    elif style.rect_mode != CORNER:
        raise ValueError(
            'glutils.style.rect_mode = {}, which is invalid'.format(
                style.rect_mode))
    return x, y, w, h

def rect_fill(x, y, w, h):
    x, y, w, h = rect_mode_convert(x, y, w, h)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

def rect_stroke(x, y, w, h):
    # TODO - change to ellipse_stroke algorithm
    x, y, w, h = rect_mode_convert(x, y, w, h)
    lw = style.stroke_weight / 2

    glBegin(GL_LINES)
    glVertex2f(x - lw, y)
    glVertex2f(x + w + lw, y)

    glVertex2f(x + w, y - lw)
    glVertex2f(x + w, y + h + lw)

    glVertex2f(x + w + lw, y + h)
    glVertex2f(x - lw, y + h)

    glVertex2f(x, y + h + lw)
    glVertex2f(x, y - lw)
    glEnd()

def ellipse_fill(x, y, a, b):
    glBegin(GL_POLYGON)
    for theta in (theta/detail * 2 * pi for theta in range(detail + 1)):
        glVertex2f(a * cos(theta) + x, b * sin(theta) + y)
    glEnd()

def ellipse_stroke(x, y, a, b):
    w  = style.stroke_weight / 2
    o_a, o_b = a + w, b + w
    i_a, i_b = a - w, b - w
    glBegin(GL_TRIANGLE_STRIP)
    for theta in (theta/detail * 2 * pi for theta in range(detail + 1)):
        glVertex2f(o_a * cos(theta) + x, o_b * sin(theta) + y)
        glVertex2f(i_a * cos(theta) + x, i_b * sin(theta) + y)

    glVertex2f(o_a + x, y)
    glEnd()