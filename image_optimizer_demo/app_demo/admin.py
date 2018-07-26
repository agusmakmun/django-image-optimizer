# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app_demo.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    list_filter = ['created']


admin.site.register(Post, PostAdmin)
