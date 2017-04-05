import copy

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from colorsys import hsv_to_rgb

rect_modes  = 'corner', 'corners', 'center', 'radius'
color_modes = 'rgb', 'hsv'

__all__ = ['Style']

class Style:
    def __init__(self):
        ''' Sets up the default style values '''
        self.fill = (1, 1, 1)
        self.stroke = (0, 0, 0)
        self.stroke_weight = 1

        self.rect_mode = 'corner'
        self.elli_mode = 'center'

        self.color_mode = 'rgb'

    def refresh(self):
        ''' will refresh something '''
        pass

    def copy(self):
        ''' returns a 'deep' copy of this object '''
        return copy.copy(self)

    # ----- color -----
    def _convert_color(self, r, g, b):
        '''
        Internal function used to convert hsv to rgb if hsv mode is set
        '''
        if self.color_mode == 'hsv':
            return hsv_to_rgb(r, g, b)
        return r, g, b

    def color(self, r, g=None, b=None):
        '''
        Attempts to convert r, g, b values to (r, g, b) floating point tuple

        rgb values can either be all integers or all floats.

        If only one value is passed, it is used as grayscale.

        If floats are passed, the range is [0, 1], if integers are passed, the
        range is [0, 255]
        '''

        # TODO - Allow 0 to be considered float or integer
        # I believe this ^ is done already, no tests.

        # Ensure that if either g or b is None, both are
        if None in (g, b) and g != b:
            raise TypeError('color() must have 1 argument or 3 arguments')

        # If r was the only argument passed in, use grayscale
        elif None in (g, b):
            if type(r) is float:
                if r < 0 or r > 1:
                    raise ValueError(
                        'color() float values must be in the range [0, 1]')
                return r, r, r
            elif type(r) is int:
                if r < 0 or r > 255:
                    raise ValueError(
                        'color() integer values must be in range [0, 255]')
                r /= 255
                return r, r, r
            else:
                raise TypeError('color() arguments must be floats or integers.')

        # If r, g, and b were all passed in
        elif {type(x) for x in (r, g, b) if x != 0} not in ({int}, {float}):
            raise TypeError(
                'color() arguments must be all floats or all integers.')

        elif type(r) is int:
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError(
                    'color() integer values must be in range [0, 255]')
            v = r / 255, g / 255, b / 255

        elif type(r) is float:
            if not (0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1):
                raise ValueError(
                    'color() float values must be in range [0, 1]')
            v = r, g, b
        return self._convert_color(*v)

    # ----- fill -----
    def set_fill(self, c):
        self.fill = self.color(*c)

    def no_fill(self):
        self.fill = 0

    def re_fill(self):
        glColor3f(*self.fill)

    # ----- stroke/stroke_weight -----
    def set_stroke(self, c):
        self.stroke = self.color(*c)

    def no_stroke(self):
        self.stroke_weight = 0

    def set_stroke_weight(self, w):
        self.stroke_weight = w

    def re_stroke(self):
        glColor3f(*self.stroke)

    # ----- shape modes -----
    def set_rect_mode(self, mode):
        self.rect_mode = mode

    # TODO
    def set_elli_mode(self, mode):
        self.elli_mode = mode

    # TODO
    def set_color_mode(self, mode):
        self.color_mode = mode
