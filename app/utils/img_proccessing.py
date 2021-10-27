from io import BytesIO
from PIL import Image
import numpy as np


def read_imagefile(file) -> Image.Image:
    """
    Parameters:
        file (binary): uploaded with fastapi.

    Returns:
        image: np array type.
    """
    image = Image.open(BytesIO(file))
    return np.asarray(image)
