from collections import defaultdict
from OpenGL.GLUT import *

handlers = [
            # mouse events
            'mouse_moved', 'mouse_dragged', 'mouse_pressed', 'mouse_released',
            'mouse_wheeled',

            # key events
            'key_pressed', 'key_released']

class Events:
    def __init__(self, condor_instance):
        self.condor = condor_instance

        # 0 if button is pressed, 1 if not pressed
        self.buttons = defaultdict(lambda: 1)
        self.mouse_x = None
        self.mouse_y = None
        self.recent_key = None

    def setup(self):
        glutPassiveMotionFunc(self.mouse_moved_handler)
        glutMotionFunc(self.mouse_dragged_handler)
        glutMouseFunc(self.mouse_clicked_handler)

        glutSpecialFunc(self.key_pressed_handler)
        glutSpecialUpFunc(self.key_released_handler)

        glutKeyboardFunc(self.key_pressed_handler)
        glutKeyboardUpFunc(self.key_released_handler)

    def is_button_pressed(self, button):
        return not bool(self.buttons[button])

    def key_pressed_handler(self, *args):
        self.key = args[0]
        self.condor.key_pressed(args[0])

    def key_released_handler(self, *args):
        self.key = args[0]
        self.condor.key_released(args[0])

    def mouse_moved_handler(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        self.condor.mouse_moved()

    def mouse_dragged_handler(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        self.condor.mouse_dragged()

    def mouse_clicked_handler(self, button, state, x, y):
        '''
        Handles clicks and scrolls.

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
        self.mouse_x = x
        self.mouse_y = y

        if button == 3 or button == 4:
            self.condor.mouse_wheeled('up' if button == 3 else 'down')
        elif state:
            self.condor.mouse_released(button)
        else:
            self.condor.mouse_pressed(button)
