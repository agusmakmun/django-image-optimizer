django-image-optimizer |pypi version|
---------------------------------------

.. |pypi version|
   image:: https://img.shields.io/pypi/v/django-image-optimizer.svg
   :target: https://pypi.python.org/pypi/django-image-optimizer

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/agusmakmun/django-image-optimizer/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/django-image-optimizer.svg
   :target: https://pypi.python.org/pypi/django-image-optimizer

.. image:: https://img.shields.io/badge/Django-1.8%20%3E=%203.0-green.svg
  :target: https://www.djangoproject.com


Django Image Optimizer is a simple Django library that allows optimization
of images by using `TinyPNG <https://tinypng.com/>`_ or `Pillow <pillow.readthedocs.io/>`_.


Installation
------------------------------

Django Image Optimizer is available directly from `PyPI <https://pypi.python.org/pypi/django-image-optimizer>`_:

1. Installing the package.

::

    $ pip install django-image-optimizer


2. Don't forget to add ``'image_optimizer'`` to your ``'INSTALLED_APPS'``.

::

    # settings.py
    INSTALLED_APPS = [
        ....
        'image_optimizer',
    ]


3. You have the option to use either TinyPNG or Pillow for optimizing images.
   Inform ``optimized_image`` which one you want to use by setting the following

::

    # To use Pillow
    OPTIMIZED_IMAGE_METHOD = 'pillow'
    # To use TinyPNG
    OPTIMIZED_IMAGE_METHOD = 'tinypng'

Any other string that is set for this setting will mean that optimization does
not occur. If you are unsure of whether you would like to use TinyPNG or Pillow,
feel free to consult the documentation of each.

If you choose to use TinyPNG, you will need to get an API key from
TinyPNG. Visit https://tinypng.com/developers for more details on getting an
API key. Once you have done so, add the following setting to your settings
file. Note: it is a good idea to keep this secret

::

    TINYPNG_KEY = 'your-key'


4. You may use the ``OptimizedImageField`` by importing it

::

    from django.db import models

    from image_optimizer.fields import OptimizedImageField


    class MyModel(models.Model):
        ...
        image = OptimizedImageField()


    class MyModel2(models.Model):
        """
        If you using OPTIMIZED_IMAGE_METHOD = 'pillow'
        You can use this optional arguments.

        This model represents a MyModel2 with a few
        fields including a `image` field which is an OptimizedImageField
        instance with `optimized_image_output_size` and
        `optimized_image_resize_method` arguments set.

        This means that image would be a resized
        version of the source image, meant to keep a given screen resolution,
        in this case (400, 300) pixels.
        """
        image = OptimizedImageField(
            upload_to='uploads/collaborators/%Y/%m/%d',
            optimized_image_output_size=(400, 300),
            optimized_image_resize_method='cover'  # 'thumbnail', 'cover' or None
        )


and saving images into it, the same way you would to a Django ``ImageField``.
The optimized image will be saved into the ``url`` field in place of the
unoptimized image.


5. Or you can directly use the ``image_optimizer`` function from utils.

::

    from image_optimizer.utils import image_optimizer


    def post_image(request):
        image_data = request.FILES.get('image')
        image_data = image_optimizer(image_data=image_data,
                                     output_size=(400, 300),
                                     resize_method='cover')
        ....


**P.S:**

 Note about TinyPNG API keys: If you obtain the free TinyPNG API token, you are limited to 500
 image optimizations per month, so this function may fail if you have a
 lot of images. You may either obtain a paid API key, or wait until next month.

This project forked from: https://github.com/dchukhin/django_optimized_image
