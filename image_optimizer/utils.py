# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO
from PIL import Image
from resizeimage import resizeimage

import tinify
import logging
import requests

from .settings import (OPTIMIZED_IMAGE_METHOD, TINYPNG_KEY)


BACKGROUND_TRANSPARENT = (255, 255, 255, 0)


def get_file_name(image_data):
    return image_data.name


def get_file_extension(file_name):
    extension = None

    # Get image file extension
    if file_name.split('.')[-1].lower() != 'jpg':
        extension = file_name.split('.')[-1].upper()
    else:
        extension = 'JPEG'

    return extension


def get_image_extension(image):
    return image.format


def image_optimizer(image_data, output_size=None, resize_method=None):
    """
    Optimize an image that has not been saved to a file.
    :param `image_data` is image data, e.g from request.FILES['image']
    :param `output_size` is float pixel scale of image (width, height) or None, e.g: (400, 300)
    :param `resize_method` is string resize method, choices are: None, "thumbnail", or "cover".
    :return optimized image data.
    """
    if OPTIMIZED_IMAGE_METHOD == 'pillow':
        image = Image.open(image_data)
        bytes_io = BytesIO()

        extension = get_image_extension(image)

        # If output_size is set, resize the image with the selected
        # resize_method. 'thumbnail' is used by default
        if output_size is not None:

            if resize_method not in ('thumbnail', 'cover', None):
                message = 'optimized_image_resize_method misconfigured, it\'s value must be \'thumbnail\', \'cover\' or None'
                raise Exception(message)

            elif resize_method is 'thumbnail':
                image = resizeimage.resize_thumbnail(image, output_size, resample=Image.LANCZOS)

            elif resize_method is 'cover':
                image = resizeimage.resize_cover(image, output_size, validate=False)

            output_image = Image.new('RGBA', output_size, BACKGROUND_TRANSPARENT)
            output_image_center = (int((output_size[0] - image.size[0]) / 2),
                                   int((output_size[1] - image.size[1]) / 2))

            output_image.paste(image, output_image_center)

        else:
            # If output_size is None the output_image would be the same as source
            output_image = image

        # If the file extension is JPEG, convert the output_image to RGB
        if extension == 'JPEG':
            output_image = output_image.convert('RGB')

        output_image.save(bytes_io, format=extension, optimize=True)

        image_data.seek(0)
        image_data.file.write(bytes_io.getvalue())
        image_data.file.truncate()

    elif OPTIMIZED_IMAGE_METHOD == 'tinypng':
        # disable warning info
        requests.packages.urllib3.disable_warnings()

        # just info for people
        if any([output_size, resize_method]):
            message = '[django-image-optimizer] "output_size" and "resize_method" only for OPTIMIZED_IMAGE_METHOD="pillow"'
            logging.info(message)

        tinify.key = TINYPNG_KEY
        optimized_buffer = tinify.from_buffer(image_data.file.read()).to_buffer()
        image_data.seek(0)
        image_data.file.write(optimized_buffer)
        image_data.file.truncate()

    return image_data
