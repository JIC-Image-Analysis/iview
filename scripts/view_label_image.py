import sys
from vispy import scene
from vispy import app
import numpy as np

from imageio import imread


colors = {
    1: [255, 0, 0],
    2: [0, 255, 0],
    3: [0, 0, 255],
    4: [255, 255, 0],
    5: [255, 0, 255],
    6: [0, 255, 255]
}

canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 800, 600
canvas.show()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()

# Create the image
# img_data = np.random.normal(size=(100, 100, 3), loc=128,
#                             scale=50).astype(np.ubyte)
img_data = imread('data/fixed_mask_1.png')
xdim, ydim = img_data.shape

im = np.zeros((xdim, ydim, 3), dtype=np.uint8)
for k, v in colors.items():
    im[np.where(img_data == k)] = v
image = scene.visuals.Image(im, parent=view.scene)

# Set 2D camera (the camera will scale to the contents in the scene)
view.camera = scene.PanZoomCamera(aspect=1)
view.camera.set_range()
view.camera.flip = (False, True, False)



if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()
