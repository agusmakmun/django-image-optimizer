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
            data = image_optimizer(data)
        super().save_form_data(instance, data)
