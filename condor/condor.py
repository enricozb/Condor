import sys
import condor.glutils as glutils
from condor.style import Style
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Condor:
    def __init__(self):
        self.looping = True
        self.style = Style()

    # ----- hidden functions -----

    def _loop(self):
        if self.looping:
            self._before_draw()
            self.draw()
            glutSwapBuffers()

    def _before_draw(self):
        self._prepare_2d(self.width, self.height)
        self._refresh_style()

    def _prepare_2d(self, width, height):
        glutils.prepare_2d(width, height)

    def _refresh_style(self):
        self.style.refresh()

    # ----- exposed functions -----

    def size(self, width, height):
        if {type(width), type(height)} != {int}:
            raise TypeError('size() arguments must be integers.')
        if width <= 1 or height <= 1:
            raise ValueError('size() width and height must be positive.')

        self.width = width
        self.height = height
        glutils.init_window('condor', width, height)

    def no_loop(self):
        self.looping = False

    def loop(self):
        self.looping = True

    # ----- style -----

    def fill(self, r, g, b):
        self.style.set_fill(r, g, b)

    def no_fill(self):
        self.style.no_fill()

    def stroke(self, r, g, b):
        if {type(r), type(g), type(g)}.difference({float, int}):
            raise TypeError('stroke() arguments must be integers or floats')
        self.style.set_stroke(r, g, b)

    def no_stroke(self):
        self.style.no_stroke()

    def stroke_weight(self, w):
        if type(w) not in (int, float):
            raise TypeError('stroke_weight() weight must be integer of float')

        if w <= 0:
            raise ValueError('stroke_weight() weight must be positive')

        self.style.set_stroke_weight(w)

    def background(self, r, g, b):
        if {type(r), type(g), type(g)}.difference({float, int}):
            raise TypeError('background() arguments must be integers or floats')
        glutils.clear_color((r, g, b))

    # ----- shapes -----

    def rect(self, x, y, w, h):
        if self.style.fill:
            self.style.re_fill()
            glutils.rect_fill(x, y, w, h)
        if self.style.stroke:
            self.style.re_stroke()
            glutils.rect_stroke(x, y, w, h, self.style.stroke_weight)

    def ellipse(self, x, y, a, b):
        if self.style.fill:
            self.style.re_fill()
            glutils.ellipse_fill(x, y, a, b)
        if self.style.stroke:
            self.style.re_stroke()
            glutils.ellipse_stroke(x, y, a, b, self.style.stroke_weight)

    def begin(self, setup, draw):
        if not (callable(setup) and callable(draw)):
            raise TypeError('begin() arguments must be functions')

        self.setup = setup
        self.draw = draw
        self.setup()
        glutSwapBuffers()
        glutils.callback(self._loop)

__all__ = list(filter(lambda x: not x.startswith('_'), Condor.__dict__))

# Expose functions:
c = Condor()
g = globals()
for func in Condor.__dict__:
    g[func] = getattr(c, func)