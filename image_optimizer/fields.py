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
                self.optimized_image_output_size
            )

        super().save_form_data(instance, data)

    def __init__(self, optimized_image_output_size=None, *args, **kwargs):
        # Set the optimized_image_output_size specified on your model
        # OptimizedImageField instances
        self.optimized_image_output_size = optimized_image_output_size

        super(OptimizedImageField, self).__init__(
            optimized_image_output_size,
            *args,
            **kwargs
        )
