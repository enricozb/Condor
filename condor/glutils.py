''' Thicker wrapper around Python OpenGL bindings '''

# TODO - eventually remove this file

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from condor.style import *

from math import pi, sin, cos

# TODO - move detail to style.py and make configurable
detail = 20
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
    if style.rect_mode == 'corners':
        if w <= x or h <= y:
            raise ValueError('For rect_mode "corners", first point must be' +
                'below and left of second point.')
        w -= x
        h -= y
    elif style.rect_mode == 'center':
        x -= w/2
        y -= h/2
    elif style.rect_mode == 'radius':
        x -= w
        y -= h
        w <<= 2
        h <<= 2
    elif style.rect_mode != 'corner':
        raise ValueError(
            'glutils.style.rect_mode = {}, which is invalid'.format(
                style.rect_mode))
    return x, y, w, h


def rect(x, y, w, h):
    if style.fill:
        style.re_fill()
        x, y, w, h = rect_mode_convert(x, y, w, h)
        glRectf(x, y, x + w, y + h)

    if style.stroke_weight:
        style.re_stroke()

        # TODO - change to ellipse_stroke algorithm?
        x, y, w, h = rect_mode_convert(x, y, w, h)
        lw = style.stroke_weight / 2

        glRectf(x - lw, y - lw, x + lw, y + h + lw)
        glRectf(x - lw, y - lw, x + w + lw, y + lw)
        glRectf(x - lw, y + h - lw, x + w + lw, y + h + lw)
        glRectf(x + w - lw, y - lw, x + w + lw, y + h + lw)

def ellipse(x, y, a, b):
    if style.fill:
        style.re_fill()

        glBegin(GL_POLYGON)
        for theta in (theta/detail * 2 * pi for theta in range(detail + 1)):
            glVertex2f(a * cos(theta) + x, b * sin(theta) + y)
        glEnd()

    if style.stroke_weight:
        style.re_stroke()

        w  = style.stroke_weight / 2
        o_a, o_b = a + w, b + w
        i_a, i_b = a - w, b - w
        glBegin(GL_TRIANGLE_STRIP)
        for theta in (theta/detail * 2 * pi for theta in range(detail + 1)):
            glVertex2f(o_a * cos(theta) + x, o_b * sin(theta) + y)
            glVertex2f(i_a * cos(theta) + x, i_b * sin(theta) + y)

        glVertex2f(o_a + x, y)
        glEnd()

def quad(points):
    a, b, c, d = points
    if style.fill:
        style.re_fill()
        glBegin(GL_TRIANGLE_STRIP)
        glVertex2f(*a)
        glVertex2f(*b)
        glVertex2f(*d)
        glVertex2f(*c)
        glEnd()

    if style.stroke_weight:
        style.re_stroke()
        glBegin(GL_TRIANGLE_STRIP)

        glEnd()

def line(a, b, c, d):
    if style.stroke_weight:
        style.re_stroke()
        v1 = c - a
        v2 = d - b

        norm = np.sqrt(v1 ** 2 + v2 ** 2) / (style.stroke_weight / 2)
        v1 /= norm
        v2 /= norm
        glBegin(GL_TRIANGLE_STRIP)
        glVertex2f(a + v2, b - v1)
        glVertex2f(a - v2, b + v1)
        glVertex2f(c + v2, d - v1)
        glVertex2f(c - v2, d + v1)
        glEnd()

curve_detail = 20
def bezier(points):
    a, b, c, d = map(np.matrix, points)

    # bezier curve
    f = lambda t: ( a * (1 - t) ** 3 +
                    b * 3 * t * (1 - t) ** 2 +
                    c * 3 * t ** 2 * (1 - t) +
                    d * t ** 3)

    # bezier derivative
    df = lambda t: (3 * (b - a) * (1 - t) ** 2 +
                    6 * (c - b) * (1 - t) * t +
                    3 * (d - c) * t ** 2)

    if style.fill:
        style.re_fill()
        glBegin(GL_POLYGON)
        for i in range(0, curve_detail + 1):
            t = i/curve_detail
            x, y = f(t).tolist()[0]
            glVertex2f(x, y)
        glEnd()

    if style.stroke_weight:
        style.re_stroke()
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(0, curve_detail + 1):
            t = i/curve_detail
            x, y = f(t).tolist()[0]
            tangent = df(t).tolist()[0]
            ortho1 = np.matrix((-tangent[1], tangent[0]))
            ortho2 = -ortho1

            n = np.linalg.norm(ortho1) / (style.stroke_weight / 2)
            ortho1 /= n
            ortho2 /= n
            glVertex2f(ortho1[0,0] + x, ortho1[0,1] + y)
            glVertex2f(ortho2[0,0] + x, ortho2[0,1] + y)
        glEnd()
