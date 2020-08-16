from PIL import Image
from random import sample

def dist(a, b):
    ''' relative distance '''
    assert(len(a) == len(b))
    return sum((x - y) ** 2 for x, y in zip(a, b))

def average(points):
    return tuple(map(lambda x: sum(x)/len(x), zip(*points)))

def find_clusters(centers, points):
    for cluster in centers.values():
        cluster.clear()
    for p in points:
        closest = min(centers, key=lambda c: dist(p, c))
        centers[closest].add(p)

def find_centers(centers):
    clusters = list(centers.values())
    centers.clear()
    for cluster in clusters:
        if cluster:
            centers[average(cluster)] = set()

def kmeans(k):
    im = Image.open('/home/enricozb/dank.jpg')
    width, height = im.size

    scale_down = 10

    im = im.resize((width//scale_down, height//scale_down))
    width, height = im.size

    im = im.convert('RGB')
    px = im.getpixel((1,1))

    points = set()

    for x in range(width):
        for y in range(height):
            points.add(im.getpixel((x, y)))

    centers = dict()

    for r, g, b in sample(points, k):
        centers[r, g, b] = set()

    return centers, points

from condor import *
import colorsys

centers, points = kmeans(10)

def setup():
    size(255, 255)
    color_mode('hsv')
    no_stroke()

def draw():
    background(35)

    find_clusters(centers, points)
    find_centers(centers)
    l = len(centers)

    for i, center in enumerate(sorted(centers)):
        h, s, v = colorsys.rgb_to_hsv(*map(lambda x: x/255, center))
        fill(h, s, v)
        rect(width() * i/l, 0, width()/l, height())

    if frame_count() > 30:
        no_loop()
        print('done')

def key_pressed(key):
    if key is b'r':
        redraw()
    if key is b'q':
        quit()
begin()

