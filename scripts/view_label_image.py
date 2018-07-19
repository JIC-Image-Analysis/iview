import sys
from vispy import scene
from vispy.scene.visuals import Text
from vispy import app
import numpy as np

from imageio import imread

import click

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


@click.command()
@click.argument('image_fpath')
def main(image_fpath):
    img_data = imread(image_fpath)
    xdim, ydim = img_data.shape

    im = np.zeros((xdim, ydim, 3), dtype=np.uint8)
    for k, v in colors.items():
        im[np.where(img_data == k)] = v
    image = scene.visuals.Image(im, parent=view.scene)

    t1 = scene.visuals.Text('Text in root scene (24 pt)', parent=image, color='red', pos=(100,100))
    t1.font_size = 24
    # Set 2D camera (the camera will scale to the contents in the scene)
    view.camera = scene.PanZoomCamera(aspect=1)
    view.camera.set_range()
    view.camera.flip = (False, True, False)

    app.run()


if __name__ == '__main__':
    main()
