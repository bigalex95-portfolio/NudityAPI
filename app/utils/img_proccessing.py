from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import requests


def read_imagefile(file, max_size=256) -> Image.Image:
    """
    Parameters:
        file (binary): uploaded with fastapi.

    Returns:
        image: np array type.
    """
    image = Image.open(BytesIO(file))
    width, height = image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = image.resize(
        (
            int(width * resize_factor),
            int(height * resize_factor),
        )
    )
    # print(resized_image.size)
    return np.asarray(resized_image)


def draw_bndbx(image, draw_details):
    colors = {}

    for detail in draw_details:
        box = detail.get("box")
        label = detail.get("label")
        if label not in colors:
            colors[label] = list(np.random.random(size=3) * 256)

        # Represents the top left corner of rectangle
        starting_point = tuple(box[:2])

        # Represents the bottom right corner of rectangle
        ending_point = tuple(box[2:])

        # Line thickness of 2 px
        thickness = 2

        # bounding box color
        box_color = colors.get(label)

        # Draw a rectangle with blue line borders of thickness of 2 px
        image = cv2.rectangle(image, starting_point,
                              ending_point, box_color, thickness)

    # print(colors)
    image = Image.fromarray(image)
    # print(image.size)
    return image


def read_image_from_url(url, max_size=256) -> Image.Image:
    """
    Parameters:
        url: url to image file.

    Returns:
        image: np array type.
    """
    image = Image.open(requests.get(url, stream=True).raw)
    width, height = image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = image.resize(
        (
            int(width * resize_factor),
            int(height * resize_factor),
        )
    )
    # print(resized_image.size)
    return np.asarray(resized_image)
