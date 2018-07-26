# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from image_optimizer.fields import OptimizedImageField


class Post(models.Model):
    title = models.CharField(max_length=100)
    photo = OptimizedImageField(upload_to='uploads/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
