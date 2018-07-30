import sys
from vispy import scene
from vispy import app
import numpy as np

from imageio import imread

from dtoolcore import DataSet

import click


def identifiers_where_overlay_is_true(dataset, overlay_name):

    overlay = dataset.get_overlay(overlay_name)

    selected = [identifier
                for identifier in dataset.identifiers
                if overlay[identifier]]

    return selected


canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 1200, 900
canvas.show()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()

# Create the image
# img_data = np.random.normal(size=(100, 100, 3), loc=128,
#                             scale=50).astype(np.ubyte)
# img_data = imread('data/T15.png')
# image2 = scene.visuals.Image(imread('data/T15-membrane-cropped.png'), parent=view.scene)
# image = scene.visuals.Image(img_data, parent=view.scene)

# image2.visible = False



@canvas.events.key_press.connect
def key_event(event):

    if event.key.name == 'Space':
        display.mask_image.visible = not display.mask_image.visible
        display.image.visible = not display.image.visible

    else:
        imid = next(display.im_ids)
        display.display_id(imid)


class Display(object):

    def display_id(self, imid):

        im = imread(self.dataset.item_content_abspath(imid))
        mask_im = imread(self.dataset.item_content_abspath(display.mask_overlay[imid]))

        display.image.set_data(im)
        display.mask_image.set_data(mask_im)

        display.t1.text = display.dataset.item_properties(imid)['relpath']

        canvas.update()


display = Display()


@click.command()
@click.argument('dataset_uri')
def main(dataset_uri):

    dataset = DataSet.from_uri(dataset_uri)

    display.im_ids = iter(identifiers_where_overlay_is_true(dataset, "is_image"))

    imid = next(display.im_ids)

    display.mask_overlay = dataset.get_overlay("mask_ids")
    im = imread(dataset.item_content_abspath(imid))
    mask_im = imread(dataset.item_content_abspath(display.mask_overlay[imid]))
    display.dataset = dataset
    display.image = scene.visuals.Image(im, parent=view.scene)
    display.mask_image = scene.visuals.Image(mask_im, parent=view.scene)
    display.mask_image.visible = False

    textstr = display.dataset.item_properties(imid)['relpath']
    t1 = scene.visuals.Text(textstr, parent=display.image, color='red', pos=(30,5))
    t1.font_size = 24
    display.t1 = t1

    view.camera = scene.PanZoomCamera(aspect=1)
    view.camera.set_range()
    view.camera.flip = (False, True, False)

    app.run()


if __name__ == '__main__' and sys.flags.interactive == 0:
    main()
