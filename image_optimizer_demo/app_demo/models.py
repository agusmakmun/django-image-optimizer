"""app_demo models."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from image_optimizer.fields import OptimizedImageField


class Post(models.Model):
    """
    Post model.

    This model represents a Blog Post with a few fields including a `photo`
    field which is an OptimizedImageField instance without any optional
    argument. This means that out Post photo would keep source image original
    size.
    """

    title = models.CharField(
        max_length=100
    )
    photo = OptimizedImageField(
        upload_to='uploads/posts/%Y/%m/%d'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
