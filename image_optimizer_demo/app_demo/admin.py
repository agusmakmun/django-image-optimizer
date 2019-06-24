# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app_demo.models import (
    Post,
    Collaborator,
)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    list_filter = ['created']


class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created']


admin.site.register(Post, PostAdmin)
admin.site.register(Collaborator, CollaboratorAdmin)
