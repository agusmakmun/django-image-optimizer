import tinify
import logging
import requests
from io import BytesIO
from PIL import Image
from resizeimage import resizeimage
from uuid import uuid4

from .settings import OPTIMIZED_IMAGE_METHOD, TINYPNG_KEY


BACKGROUND_TRANSPARENT = (255, 255, 255, 0)


def get_file_name(image_data):
    return image_data.name


def get_file_extension(file_name):
    extension = None
    # Get image file extension
    if file_name.split(".")[-1].lower() != "jpg":
        extension = file_name.split(".")[-1].upper()
    else:
        extension = "JPEG"
    return extension


def get_image_extension(image):
    return image.format


def image_optimizer(image_data, output_size=None, resize_method=None):
    """
    Optimize an image that has not been saved to a file.
    :param `image_data` is image data, e.g from request.FILES['image']
    :param `output_size` is float pixel scale of image (width, height) or None, for example: (400, 300) # noqa: E501
    :param `resize_method` is string resize method, choices are:
            None or resizeimage.resize() method argument values,
            i.e: "crop", "cover", "contain", "width", "height", "thumbnail"
    :return optimized image data.
    """
    if OPTIMIZED_IMAGE_METHOD == "pillow":
        image = Image.open(image_data)
        bytes_io = BytesIO()

        extension = get_image_extension(image)

        # If output_size is set, resize the image with the selected
        # resize_method. 'thumbnail' is used by default
        if output_size is not None:
            if resize_method:
                image = resizeimage.resize(
                    method=resize_method,
                    image=image,
                    size=output_size,
                )

            output_image = Image.new(
                "RGBA",
                output_size,
                BACKGROUND_TRANSPARENT,
            )
            output_image_center = (
                int((output_size[0] - image.size[0]) / 2),
                int((output_size[1] - image.size[1]) / 2),
            )
            output_image.paste(image, output_image_center)
        else:
            # If output_size is None the output_image
            # would be the same as source
            output_image = image

        # If the file extension is JPEG, convert the output_image to RGB
        if extension == "JPEG":
            output_image = output_image.convert("RGB")

        output_image.save(bytes_io, format=extension, optimize=True)

        image_data.seek(0)
        image_data.file.write(bytes_io.getvalue())
        image_data.file.truncate()

    elif OPTIMIZED_IMAGE_METHOD == "tinypng":
        # disable warning info
        requests.packages.urllib3.disable_warnings()

        # just info for people
        if any([output_size, resize_method]):
            message = (
                '[django-image-optimizer] "output_size" and "resize_method" '
                'only for OPTIMIZED_IMAGE_METHOD="pillow"'
            )
            logging.info(message)

        tinify.key = TINYPNG_KEY
        optimized_buffer = tinify.from_buffer(
            image_data.file.read()
        ).to_buffer()  # noqa: E501
        image_data.seek(0)
        image_data.file.write(optimized_buffer)
        image_data.file.truncate()

    return image_data


def crop_image_on_axis(image, width, height, x, y, extension):
    """
    function to crop the image using axis (using Pillow).
    :param `image` is image data, e.g from request.FILES['image']
    :param `width` float width of image
    :param `height` float height of image
    :param `x` is float x axis
    :param `y` is float y axis
    :param `extension` is string, e.g: ".png"
    """
    # Open the passed image
    img = Image.open(image)

    # Initialise bytes io
    bytes_io = BytesIO()

    # crop the image through axis
    img = img.crop((x, y, width + x, height + y))

    # resize the image and optimise it for file size,
    # making smaller as possible
    img = img.resize((width, height), Image.ANTIALIAS)

    # This line is optional, for safe side, image name should be unique.
    img.name = "{}.{}".format(uuid4().hex, extension)

    # If the file extension is JPEG, convert the output_image to RGB
    if extension == "JPEG":
        img = image.convert("RGB")
    img.save(bytes_io, format=extension, optimize=True)

    # return the image
    image.seek(0)

    # Write back new image
    image.file.write(bytes_io.getvalue())

    # truncate the file size
    image.file.truncate()
    return image
