from condor import *
from condor.profile import timing

from math import sin, cos

fr = 60

def setup():
    size(500, 500)
    rect_mode('center')

    fill(1.0, 0, 0)     # red
    stroke(0, 1.0, 0)   # green

    frame_rate(100)

    stroke_weight(20)

    print("Scroll wheel to change frame_rate")

def draw():
    background(35)
    w = 50 * sin(frame_count()/100) + 100
    h = 50 * cos(frame_count()/100) + 100
    rect(width()/2, height()/2, w, h)

def mouse_wheeled(direction):
    global fr
    if direction == 'up':
        fr += 10
    else:
        fr -= 10
    frame_rate(fr)
    print(fr)

begin()

