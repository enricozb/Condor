from OpenGL.GLUT import *

handlers = ['mouse_moved', 'mouse_dragged', 'mouse_pressed', 'mouse_released']

class Events:
    def __init__(self, condor_instance):
        self.condor = condor_instance

        # event attributes

        # 0 if button is pressed, 1 if not pressed
        self.buttons = [1] * 5
        self.mouse_x = None
        self.mouse_y = None

    def setup(self):
        glutPassiveMotionFunc(self.mouse_moved_handler)
        glutMotionFunc(self.mouse_dragged_handler)
        glutMouseFunc(self.mouse_clicked_handler)

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

        if state:
            self.condor.mouse_pressed()
        else:
            self.condor.mouse_released()
