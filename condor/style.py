from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# ----- style constants -----

# shape modes
CORNER      = 1 << 0
CORNERS     = 1 << 1
CENTER      = 1 << 2
RADIUS      = 1 << 3

# color modes
RGB         = 1 << 4

class Style:
    def __init__(self):
        ''' Sets up the default style values '''
        self.fill = (1, 1, 1)
        self.stroke = (0, 0, 0)
        self.stroke_weight = 1

        self.rect_mode = CORNERS
        self.elli_mode = CENTER

        self.color_mode = RGB

    def refresh(self):
        ''' will refresh something '''
        pass

    # ----- fill -----
    def set_fill(self, r, g, b):
        self.fill = r, g, b

    def no_fill(self):
        self.fill = None

    def re_fill(self):
        glColor3f(*self.fill)

    # ----- stroke/stroke_weight -----
    def set_stroke(self, r, g, b):
        self.stroke = r, g, b

    def no_stroke(self):
        self.stroke = None

    def set_stroke_weight(self, w):
        self.stroke_weight = w

    def re_stroke(self):
        glColor3f(*self.stroke)
        # glLineWidth(self.stroke_weight)

    # ----- shape modes -----
    def set_rect_mode(self, mode):
        self.rect_mode = mode

    def set_elli_mode(self, mode):
        self.elli_mode = mode

    def set_color_mode(self, mode):
        self.color_mode = mode
