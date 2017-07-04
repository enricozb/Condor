from inspect import signature

from OpenGL.GLUT import *

handlers = [
            # mouse events
            'mouse_moved', 'mouse_dragged', 'mouse_pressed', 'mouse_released',
            'mouse_wheeled',

            # key events
            'key_pressed', 'key_released']

mouse_buttons = ['left', 'wheel', 'right']

class Events:
    def __init__(self, condor_instance):
        self.condor = condor_instance

        # 0 if button is pressed, 1 if not pressed
        self.buttons = [1] * 5
        self.mouse_x = 0
        self.mouse_y = 0
        self.recent_key = None

    def _convert_button(self, button):
        if button == 'left':
            return 0
        if button == 'wheel':
            return 1
        if button == 'right':
            return 2
        raise ValueError('Invalid button {}'.format(button))

    def call_func(self, func, kwargs):
        kwargs = {x : y for x, y in kwargs.items()
                        if x in signature(func).parameters}
        func(**kwargs)

    def setup(self):
        glutPassiveMotionFunc(self.mouse_moved_handler)
        glutMotionFunc(self.mouse_dragged_handler)
        glutMouseFunc(self.mouse_clicked_handler)

        glutSpecialFunc(self.key_pressed_handler)
        glutSpecialUpFunc(self.key_released_handler)

        glutKeyboardFunc(self.key_pressed_handler)
        glutKeyboardUpFunc(self.key_released_handler)

    def mouse(self, x, y):
        self.mouse_x = x
        self.mouse_y = self.condor._width - y

    def buttons_down(self, buttons):
        if not len(buttons):
            return not all(self.buttons)
        return not all(self.buttons[self._convert_button(x)] for x in buttons)

    def key_pressed_handler(self, *args):
        args = {k : v for k, v in zip(('key', 'x', 'y'), args)}
        self.call_func(self.condor.key_pressed, args)

    def key_released_handler(self, *args):
        args = {k : v for k, v in zip(('key', 'x', 'y'), args)}
        self.call_func(self.condor.key_released, args)

    def mouse_moved_handler(self, x, y):
        self.mouse(x, y)
        self.condor.mouse_moved()

    def mouse_dragged_handler(self, x, y):
        self.mouse(x, y)
        self.call_func(self.condor.mouse_dragged, {'x': x, 'y': y})

    def mouse_clicked_handler(self, button, state, x, y):
        '''
        Handles presses/releases and scrolls.

        Arguments:
            button - the 'button' that was pressed/scrolled
                0 - left mouse button
                1 - wheel click
                2 - right mouse button
                3 - wheel up
                4 - wheel down

            state - whether the button was pressed or released
                0 - pressed
                1 - released
        '''
        self.buttons[button] = state
        self.mouse(x, y)

        if 0 <= button <= 2:
            button = mouse_buttons[button]

        if button == 3 or button == 4:
            self.call_func(self.condor.mouse_wheeled,
                      {'direction' : 'up' if button == 3 else 'down'})
        elif state:
            self.call_func(self.condor.mouse_released, {'button' : button})
        else:
            self.call_func(self.condor.mouse_pressed, {'button' : button})
