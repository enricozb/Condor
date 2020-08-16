from condor import *

def setup():
    size(500, 500)
    fill(1.0, 0, 0)
    stroke(0, 1.0, 0)
    stroke_weight(20) 
    
def draw():
    background(35)
    polygon((mouse_x(), mouse_y()), (100, 200), (200, 200), (200, 100))

begin()
