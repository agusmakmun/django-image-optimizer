# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

OPTIMIZED_IMAGE_METHOD = getattr(settings, 'OPTIMIZED_IMAGE_METHOD', 'pillow')
TINYPNG_KEY = getattr(settings, 'TINYPNG_KEY', None)
