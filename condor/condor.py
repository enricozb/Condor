import condor.glutils as glutils
import condor.style
from condor.style import *

import noise as noise_module

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Condor:
    def __init__(self):
        self.looping = True
        self.style = Style()
        self._frame_count = 0
        glutils.set_style(self.style)

    # ----- hidden functions -----
    def _loop(self):
        if self.looping:
            self._before_draw()
            self.draw()
            glutSwapBuffers()
            self._frame_count += 1
        glutReshapeWindow(self._width, self._height)

    def _before_draw(self):
        self._prepare_2d(self._width, self._height)
        self._refresh_style()

    def _prepare_2d(self, width, height):
        glutils.prepare_2d(width, height)

    def _refresh_style(self):
        self.style.refresh()

    # ----- properties -----
    def frame_count(self):
        return self._frame_count

    def width(self):
        return self._width

    def height(self):
        return self._height

    # ----- exposed functions -----
    def size(self, width, height):
        if {type(width), type(height)} != {int}:
            raise TypeError('size() arguments must be integers.')
        if width <= 1 or height <= 1:
            raise ValueError('size() width and height must be positive.')

        self._width = width
        self._height = height
        glutils.init_window('condor', self._width, self._height)

    def no_loop(self):
        self.looping = False

    def loop(self):
        self.looping = True

    # ----- style -----
    def fill(self, r, g=None, b=None):
        self.style.set_fill((r, g, b))

    def no_fill(self):
        self.style.no_fill()

    def stroke(self, r, g=None, b=None):
        self.style.set_stroke((r, g, b))

    def no_stroke(self):
        self.style.no_stroke()

    def stroke_weight(self, w):
        if type(w) not in (int, float):
            raise TypeError('stroke_weight() weight must be integer or float')

        if w <= 0:
            raise ValueError('stroke_weight() weight must be positive')

        self.style.set_stroke_weight(w)

    def rect_mode(self, mode):
        if mode not in ('corner', 'corners', 'center', 'radius'):
            raise ValueError('rect_mode() called with invalid rect mode')
        self.style.set_rect_mode(mode)

    def color_mode(self, mode):
        if mode not in condor.style.color_modes:
            raise ValueError('color_mode() called with invalid color mode')
        self.style.set_color_mode(mode)

    def background(self, r, g=None, b=None):
        glutils.clear_color(self.style.color(r, g, b))

    # ----- shapes -----
    def rect(self, x, y, w, h):
        if not set(map(type, (x, y, w, h))) <= {int, float}:
            raise TypeError('rect() arguments must be integers or floats')

        if w < 0 or h < 0:
            raise ValueError('rect() width and height must be positive')

        if self.style.fill:
            self.style.re_fill()
            glutils.rect_fill(x, y, w, h)
        if self.style.stroke:
            self.style.re_stroke()
            glutils.rect_stroke(x, y, w, h)

    def ellipse(self, x, y, a, b):
        if not {type(i) for i in (x, y, a, b)} <= {int, float}:
            raise TypeError('ellipse() arguments must be integers or floats')

        if a < 0 or b < 0:
            raise ValueError('ellipse() arguments a and b must be positive')

        if self.style.fill:
            self.style.re_fill()
            glutils.ellipse_fill(x, y, a, b)
        if self.style.stroke:
            self.style.re_stroke()
            glutils.ellipse_stroke(x, y, a, b)

    def begin(self, setup, draw):
        if not (callable(setup) and callable(draw)):
            raise TypeError('begin() arguments must be functions')

        self.setup = setup
        self.draw = draw
        self.setup()
        glutSwapBuffers()
        glutils.callback(self._loop)

    # ----- random -----
    def noise(self, *args):
        if not set(map(type, args)) <= {int, float}:
            raise TypeError('noise() arguments must be integers or floats')
        if 1 <= len(args) <= 4:
            return getattr(noise_module, 'pnoise{}'.format(len(args)))(*args)
        raise ValueError('noise() must have one to four arguments')

__all__ = list(filter(lambda x: not x.startswith('_'), Condor.__dict__))

# Expose functions:
c = Condor()
g = globals()
for func in Condor.__dict__:
    g[func] = getattr(c, func)