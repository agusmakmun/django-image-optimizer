# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import ImageField


class OptimizedImageField(ImageField):
    """An ImageField that gets optimized on save() using tinyPNG."""

    def save_form_data(self, instance, data):
        """Remove the OptimizedNotOptimized object on clearing the image."""
        # Are we updating an image?
        updating_image = True if data and getattr(instance, self.name) != data else False

        if updating_image:
            from .utils import image_optimizer
            data = image_optimizer(
                data,
                self.optimized_image_output_size,
                self.optimized_image_resize_method
            )

        super().save_form_data(instance, data)

    def __init__(self, optimized_image_output_size=None,
                 optimized_image_resize_method=None, *args, **kwargs):
        # Set the optimized_image_output_size specified on your
        # OptimizedImageField model instances
        self.optimized_image_output_size = optimized_image_output_size
        # Set the optimized_image_resize_method specified on your
        # OptimizedImageField model instances
        self.optimized_image_resize_method = optimized_image_resize_method

        super().__init__(**kwargs)
