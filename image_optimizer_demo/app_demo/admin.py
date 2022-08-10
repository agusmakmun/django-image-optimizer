from django.contrib import admin
from app_demo.models import (
    Post,
    Collaborator,
    OtherImage,
)
from app_demo.forms import CropImageAxisForm


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created"]
    list_filter = ["created"]


class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]
    list_filter = ["created"]


class CropImageAxisAdmin(admin.ModelAdmin):
    list_display = ["created", "image"]
    list_filter = ["created"]
    form = CropImageAxisForm

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.request = request
        return form


admin.site.register(Post, PostAdmin)
admin.site.register(Collaborator, CollaboratorAdmin)
admin.site.register(OtherImage, CropImageAxisAdmin)
