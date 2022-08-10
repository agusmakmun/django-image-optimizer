from .models import Post
from django import forms

class PostForm(forms.ModelForm):
    width = forms.IntegerField(required=True,)
    height = forms.IntegerField(required=True)
    x = forms.FloatField( required=True)
    y = forms.FloatField( required=True)
    class Meta:
        model = Post
        fields = ("photo", "title")
