from pathlib import Path

import sys
from vispy import scene
from vispy import app
import numpy as np

from imageio import imread

import click

from dtoolcore import DataSet


canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 800, 600
canvas.show()

view = canvas.central_widget.add_view()

key_to_tag = {
    'Q': 'dormant',
    'P': 'emerged'
}

@canvas.events.key_press.connect
def key_event(event):

    app.tags[app.current_id] = key_to_tag[event.key.name]

    try:
        im, app.current_id = next(app.image_generator)
        app.image.set_data(im)
        canvas.update()
    except StopIteration:
        app.dataset.put_overlay("classes", app.tags)
        app.quit()


def dataset_image_generator(dataset):

    for i in dataset.identifiers:
        yield imread(dataset.item_content_abspath(i)), i


@click.command()
@click.argument("dataset_uri")
def main(dataset_uri):

    dataset = DataSet.from_uri(dataset_uri)
    app.dataset = dataset
    app.tags = {}

    app.image_generator = dataset_image_generator(dataset)

    im, app.current_id = next(app.image_generator)
    app.image = scene.visuals.Image(im, parent=view.scene)

    view.camera = scene.PanZoomCamera(aspect=1)
    view.camera.set_range()
    view.camera.flip = (False, True, False)

    app.run()


if __name__ == '__main__':
    main()