''' Thicker wrapper around Python OpenGL bindings '''

import numpy as np
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import condor.profile as profile

from math import pi, sin, cos

from PIL import Image

class GLUtil:
    def __init__(self, condor_instance):
        self.condor = condor_instance

    def init_window(self, title):
        ''' Creates window with title and width, height '''

        width, height = self.condor._width, self.condor._height

        if not (type(width) == type(height) == int):
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

    def draw(self):
        self.prepare_2d()
        draw_time = profile.time(self.condor.draw)
        sleep_time = 1/self.condor._frame_rate - draw_time

        # force proper framerate
        if sleep_time > 0:
            time.sleep(sleep_time)

        glutSwapBuffers()

    def begin(self, loop):
        glutDisplayFunc(loop)
        glutIdleFunc(loop)
        glutMainLoop()

    def prepare_2d(self):
        ''' Prepares for 2d rendering '''
        # TODO - Not likely modern OpenGL
        glViewport(0, 0, self.condor._width, self.condor._height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.condor._width, 0.0, self.condor._height, 0.0, 1.0)

    def background(self, color):
        glClearColor(*color, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def rect_mode_convert(self, x, y, w, h):
        if self.condor.style.rect_mode == 'corners':
            if w <= x or h <= y:
                raise ValueError('For rect_mode "corners", first point must be' +
                    'below and left of second point.')
            w -= x
            h -= y
        elif self.condor.style.rect_mode == 'center':
            x -= w/2
            y -= h/2
        elif self.condor.style.rect_mode == 'radius':
            x -= w
            y -= h
            w <<= 2
            h <<= 2
        elif self.condor.style.rect_mode != 'corner':
            raise ValueError(
                'glutils.style.rect_mode = {}, which is invalid'.format(
                    self.condor.style.rect_mode))
        return x, y, w, h

    def save_frame(self, filename):
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0,0, self.condor._width, self.condor._height,
                              GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes('RGB',
                                (self.condor._width, self.condor._height),
                                pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        split = list(filter(None, filename.split('#')))
        pad = len(filename) - len(''.join(split))
        filename = (split[0] + str(self.condor._frame_count).zfill(pad) +
                    split[1])
        image.save(filename, compress_level=0, quality=95)

    def rect(self, x, y, w, h):
        x, y, w, h = self.rect_mode_convert(x, y, w, h)
        if self.condor.style.fill:
            self.condor.style.re_fill()
            glRectf(x, y, x + w, y + h)

        if self.condor.style.stroke_weight:
            self.condor.style.re_stroke()

            # TODO - change to ellipse_stroke algorithm?
            lw = self.condor.style.stroke_weight / 2

            glRectf(x - lw, y - lw, x + lw, y + h + lw)
            glRectf(x - lw, y - lw, x + w + lw, y + lw)
            glRectf(x - lw, y + h - lw, x + w + lw, y + h + lw)
            glRectf(x + w - lw, y - lw, x + w + lw, y + h + lw)

    def ellipse(self, x, y, a, b):
        if self.condor.style.fill:
            self.condor.style.re_fill()

            glBegin(GL_POLYGON)
            for theta in (theta/self.condor.style.detail * 2 * pi
                          for theta in range(self.condor.style.detail + 1)):
                glVertex2f(a * cos(theta) + x, b * sin(theta) + y)
            glEnd()

        if self.condor.style.stroke_weight:
            self.condor.style.re_stroke()

            w  = self.condor.style.stroke_weight / 2
            o_a, o_b = a + w, b + w
            i_a, i_b = a - w, b - w
            glBegin(GL_TRIANGLE_STRIP)
            for theta in (theta/self.condor.style.detail * 2 * pi
                          for theta in range(self.condor.style.detail + 1)):
                glVertex2f(o_a * cos(theta) + x, o_b * sin(theta) + y)
                glVertex2f(i_a * cos(theta) + x, i_b * sin(theta) + y)

            glVertex2f(o_a + x, y)
            glEnd()

    def quad(self, points):
        a, b, c, d = points
        if self.condor.style.fill:
            self.condor.style.re_fill()
            glBegin(GL_TRIANGLE_STRIP)
            glVertex2f(*a)
            glVertex2f(*b)
            glVertex2f(*d)
            glVertex2f(*c)
            glEnd()

        if self.condor.style.stroke_weight:
            self.condor.style.re_stroke()
            glBegin(GL_TRIANGLE_STRIP)
                        
            glEnd()

    def polygon(self, points):
        if self.condor.style.fill:
            self.condor.style.re_fill()
            glBegin(GL_POLYGON)
            for p in points:
                glVertex2f(*p)
            glEnd()

        if self.condor.style.stroke:
            self.condor.style.re_stroke()
            glBegin(GL_TRIANGLE_STRIP)

            a, b = points[-2:] 
            for c in points:
                
                a, b = b, c

            glEnd()

    def line(self, a, b, c, d):
        if self.condor.style.stroke_weight:
            self.condor.style.re_stroke()
            v1 = c - a
            v2 = d - b

            norm = np.sqrt(v1 ** 2 + v2 ** 2) / (self.condor.style.stroke_weight / 2)
            v1 /= norm
            v2 /= norm
            glBegin(GL_TRIANGLE_STRIP)
            glVertex2f(a + v2, b - v1)
            glVertex2f(a - v2, b + v1)
            glVertex2f(c + v2, d - v1)
            glVertex2f(c - v2, d + v1)
            glEnd()

    def bezier(self, points):
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

        if self.condor.style.fill:
            self.condor.style.re_fill()
            glBegin(GL_POLYGON)
            for i in range(0, self.condor.style.curve_detail + 1):
                t = i/self.condor.style.curve_detail
                x, y = f(t).tolist()[0]
                glVertex2f(x, y)
            glEnd()

        if self.condor.style.stroke_weight:
            self.condor.style.re_stroke()
            glBegin(GL_TRIANGLE_STRIP)
            for i in range(0, self.condor.style.curve_detail + 1):
                t = i/self.condor.style.curve_detail
                x, y = f(t).tolist()[0]
                tangent = df(t).tolist()[0]
                ortho1 = np.matrix((-tangent[1], tangent[0]))
                ortho2 = -ortho1

                n = np.linalg.norm(ortho1) / (self.condor.style.stroke_weight / 2)
                ortho1 /= n
                ortho2 /= n
                glVertex2f(ortho1[0,0] + x, ortho1[0,1] + y)
                glVertex2f(ortho2[0,0] + x, ortho2[0,1] + y)
            glEnd()

