# Condor
A Processing pseudo-clone for Python which intends to improve on Processing.py.

## Usage
Currently, the easiest way to use Condor is to perform `from condor import *`
as the first import statement, and the last line of the file should be
`begin()`. This way, all Condor functions are exposed in the global namespace.
If you prefer everything be under the `condor` namespace, you can do
`import condor` instead, and call `condor.begin()`. Here is an example using
the first approach,

```python
from condor import *

def setup():
    global s_x, s_y
    size(500, 500)
    color_mode('hsv')
    no_stroke()

    scale_x = width()/r
    scale_y = height()/r

r = 50
def draw():
    background(35)
    for x in range(r):
        for y in range(r):
            n = noise(x/r * 5, y/r * 5, frame_count()/50)
            fill(n, 1.0, 1.0)
            rect(x * scale_x, y * scale_y, n * 6, n * 6)

begin()
```

## Why?
Processing is a fantastic improvement over Java syntax when it comes to any
sort of graphical programming environment. However, when simply porting its
behavior to Python syntax, I believe it degrades Python's simplicity. Python's
nice I/O is bogged down by the Processing I/O specification. I also want to
have Python 3 support and I want the freedom to easily use other editors.
