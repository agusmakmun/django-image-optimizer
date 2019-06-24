# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO
from PIL import Image
from resizeimage import resizeimage

import tinify
import requests

from .settings import (OPTIMIZED_IMAGE_METHOD, TINYPNG_KEY)

BACKGROUND_TRANSPARENT = (255, 255, 255, 0)


def get_file_extension(file_name):
    extension = None

    # Get image file extension
    if file_name.split('.')[-1].lower() != 'jpg':
        extension = file_name.split('.')[-1].upper()
    else:
        extension = 'JPEG'

    return extension


def image_optimizer(image_data, output_size=None, resize_method=None):
    """Optimize an image that has not been saved to a file."""
    if OPTIMIZED_IMAGE_METHOD == 'pillow':
        image = Image.open(image_data)
        bytes_io = BytesIO()

        file_name = image_data.name
        extension = get_file_extension(file_name)

        # If output_size is set, resize the image with the selected
        # resize_method. 'thumbnail' is used by default
        if output_size is not None:

            if resize_method is None:
                pass

            elif resize_method is 'thumbnail':
                image = resizeimage.resize_thumbnail(
                    image,
                    output_size,
                    resample=Image.LANCZOS
                )

            elif resize_method is 'cover':
                image = resizeimage.resize_cover(
                    image,
                    output_size,
                    validate=False
                )

            else:
                raise Exception(
                    'optimized_image_resize_method misconfigured, it\'s value must be \'thumbnail\', \'cover\' or None'
                )

            output_image = Image.new(
                'RGBA',
                output_size,
                BACKGROUND_TRANSPARENT
            )

            output_image_center = (
                int((output_size[0] - image.size[0]) / 2),
                int((output_size[1] - image.size[1]) / 2)
            )

            output_image.paste(
                image,
                output_image_center
            )

        # If output_size is None the output_image would be the same as source
        else:
            output_image = image

        # If the file extension is JPEG, convert the output_image to RGB
        if extension == 'JPEG':
            output_image = output_image.convert("RGB")

        output_image.save(
            bytes_io,
            format=extension,
            optimize=True
        )

        image_data.seek(0)
        image_data.file.write(bytes_io.getvalue())
        image_data.file.truncate()

    elif OPTIMIZED_IMAGE_METHOD == 'tinypng':
        # disable warning info
        requests.packages.urllib3.disable_warnings()

        tinify.key = TINYPNG_KEY
        optimized_buffer = tinify.from_buffer(image_data.file.read()).to_buffer()
        image_data.seek(0)
        image_data.file.write(optimized_buffer)
        image_data.file.truncate()
    return image_data
