from pathlib import Path

import sys
from vispy import scene
from vispy import app
import numpy as np

from imageio import imread



canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 800, 600
canvas.show()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()

# Create the image
# img_data = np.random.normal(size=(100, 100, 3), loc=128,
#                             scale=50).astype(np.ubyte)
tags = {}
imdir = Path(sys.argv[1])
fn_iter = imdir.iterdir()
fn = next(fn_iter)
im = imread(fn)
image = scene.visuals.Image(im, parent=view.scene)

# Set 2D camera (the camera will scale to the contents in the scene)
view.camera = scene.PanZoomCamera(aspect=1)
view.camera.set_range()
view.camera.flip = (False, True, False)

key_to_tag = {
    'Q': 'dormant',
    'P': 'emerged'
}

@canvas.events.key_press.connect
def key_event(event):
    global fn
    tags[fn] = key_to_tag[event.key.name]
    try:
        fn = next(fn_iter)
    except StopIteration:
        with open('tags.txt', 'w') as fh:
            for fn, tag in tags.items():
                fh.write('{},{}\n'.format(fn, tag))
        app.quit()

    image.set_data(imread(fn))
    canvas.update()

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()
