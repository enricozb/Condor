from condor import *

def setup():
    size(500, 500)

    fill(1.0, 0, 0)     # red
    stroke(0, 1.0, 0)   # green

    stroke_weight(20)

def draw():
    background(35)
    bezier((0, 0), (100, 100), (30, 40), (mouse_x(), mouse_y()))

begin()

