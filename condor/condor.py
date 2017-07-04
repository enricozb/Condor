# TODO - change glutils to modern openGL
#      - remove all OpenGL calls from condor.py

import condor.events as events
import condor.glutil as glutil
import condor.profile as profile
import condor.style as style

import noise as noise_module

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Condor:
    def __init__(self):
        self.style = style.Style()
        self.styles = []
        self.events = events.Events(self)
        self.glutil = glutil.GLUtil(self)

        self._looping = True
        self._frame_count = 0
        self._frame_rate = 60
        self._actual_frame_rate = 0
        self._redraw = 0
        self._noise_params = {
            'seed' : 0,
            'octaves' : 4,
            'persistence' : 0.5,
        }

    # should only be used during condor development
    def members(self):
        return self

    # ----- hidden functions -----
    def _dummy_function(self, *args, **kwargs):
        '''
        Called when no handlers are available for events
        '''

    def _loop(self):
        '''
        The main loop which makes call to the user's draw function.
        Notice the users draw function is always called at least once,
        as the first frame must be rendered.
        '''
        if self._looping or self._frame_count == 0 or self._redraw > 0:
            self._actual_frame_rate = 1 / profile.time(self.glutil.draw)
            self._frame_count += 1
            if self._redraw > 0:
                self._redraw -= 1
        glutReshapeWindow(self._width, self._height)

    def _setup_funcs(self, funcs):
        for func_name in events.handlers:
            self.__dict__[func_name] = self._dummy_function

        allowed_funcs = ['setup', 'draw'] + events.handlers

        for func in funcs:
            if func.__name__ in allowed_funcs:
                self.__dict__[func.__name__] = func

    # ----- image -----
    def save_frame(self, filename):
        self.glutil.save_frame(filename)

    # ----- properties -----
    def frame_count(self):
        return self._frame_count

    def frame_rate(self, fps=None):
        if fps is None:
            return self._actual_frame_rate
        self._frame_rate = fps

    def width(self):
        return self._width

    def height(self):
        return self._height

    # ----- exposed functions -----
    def size(self, width, height):
        self._width = width
        self._height = height
        self.glutil.init_window('condor')

        # TODO - move this call elsewhere
        self.events.setup()

    def no_loop(self):
        self._looping = False

    def loop(self):
        self._looping = True

    def redraw(self):
        self._redraw += 1

    def push_style(self):
        self.styles.append(self.style)
        self.style = self.style.copy()

    def pop_style(self):
        self.style = self.styles.pop()

    # ----- color -----
    def background(self, r, g=None, b=None):
        self.glutil.background(self.style.color(r, g, b))

    def fill(self, r, g=None, b=None):
        self.style.set_fill((r, g, b))

    def no_fill(self):
        self.style.no_fill()

    def stroke(self, r, g=None, b=None):
        self.style.set_stroke((r, g, b))

    def no_stroke(self):
        self.style.no_stroke()

    def stroke_weight(self, weight):
        self.style.set_stroke_weight(weight)

    def rect_mode(self, mode):
        self.style.set_rect_mode(mode)

    def color_mode(self, mode):
        self.style.set_color_mode(mode)

    def detail(self, detail):
        self.style.set_detail(detail)

    def curve_detail(self, curve_detail):
        self.style.set_curve_detail(curve_detail)

    # ----- shapes -----
    def rect(self, a, b, c, d):
        '''
        Draws a rectangle.
        Arguments must be floats or integers.
        '''
        self.glutil.rect(a, b, c, d)

    def ellipse(self, x, y, a, b):
        '''
        Draws an ellipse.
        Arguments must be floats or integers.
        '''
        self.glutil.ellipse(x, y, a, b)


    def quad(self, *points):
        '''
        Draws a quadrilateral.
        Arguments must be floats or integers.
        '''
        self.glutil.quad(points)

    def polygon(self, *points):
        '''
        Draws a polygon.
        Arguments must be floats or integers.
        '''
        self.glutil.polygon(points)

    def line(self, a, b, c, d):
        '''
        Draws a line from (a, b) to (c, d). Uses stroke property, not fill.
        Arguments must be floats or integers.
        '''
        self.glutil.line(a, b, c, d)

    # ----- entry point -----
    def begin(self, *funcs):
        '''
        Sets up all function calls, using the file that called begin() as
        the source of functions.

        Arguments must at least contain setup and draw functions.
        '''
        if not funcs:
            import __main__, inspect

            # TODO - dynamic lookup of module
            funcs = inspect.getmembers(__main__, inspect.isfunction)
            funcs = map(lambda x: x[1], funcs)

        self._setup_funcs(funcs)

        self.setup()
        glutSwapBuffers()
        self.glutil.begin(self._loop)

    # ----- random -----
    def noise(self, x, y=0, z=0):
        ''' Perlin noise '''
        seed = self._noise_params['seed']
        x += seed
        y += seed
        z += seed
        return (noise_module.pnoise3(x, y, z, octaves=4) + 1)/2

    def noise_params(self, octaves, persistence):
        self._noise_params['octaves'] = octaves
        self._noise_params['persistence'] = persistence

    def noise_seed(self, seed):
        ''' Seed perlin noise by shifting the coordinates by seed '''
        self._noise_params['seed'] = seed

    # ----- events -----
    def recent_key(self):
        return self.events.key

    def mouse_x(self):
        return self.events.mouse_x

    def mouse_y(self):
        return self.events.mouse_y

    def mouse_down(self, *buttons):
        return self.events.buttons_down(buttons)

    # ----- curves -----
    def bezier(self, *args):
        self.glutil.bezier(args)

# Expose functions:
c = Condor()
g = globals()
for func in Condor.__dict__:
    g[func] = getattr(c, func)

