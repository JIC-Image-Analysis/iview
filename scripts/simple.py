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
img_data = imread('data/sample0.jpg')
image2 = scene.visuals.Image(imread('data/padded.png'), parent=view.scene)
image = scene.visuals.Image(img_data, parent=view.scene)

image2.visible = False

# Set 2D camera (the camera will scale to the contents in the scene)
view.camera = scene.PanZoomCamera(aspect=1)
view.camera.set_range()

@canvas.events.key_press.connect
def key_event(event):
	image.visible = not image.visible
	image2.visible = not image2.visible


if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()
