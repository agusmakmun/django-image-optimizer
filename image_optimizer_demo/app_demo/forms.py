from django import forms
from .models import OtherImage
from image_optimizer.utils import crop_image_on_axis, get_file_extension


class CropImageAxisForm(forms.ModelForm):
    width = forms.IntegerField()
    height = forms.IntegerField()
    x = forms.FloatField()
    y = forms.FloatField()

    def save(self, commit=True):
        instance = super().save(commit=False)
        request = self.request

        # process on create only
        image = request.FILES.get("image")
        if image is not None:
            width = float(request.POST["width"])
            height = float(request.POST["height"])
            x = float(request.POST["x"])
            y = float(request.POST["y"])
            extension = get_file_extension(image.name)

            try:
                image = crop_image_on_axis(image, width, height, x, y, extension)
            except ValueError as error:
                raise forms.ValidationError(error)

            instance.image = image
            instance.save()
            return instance

        return super().save(commit)

    class Meta:
        model = OtherImage
        fields = ["image"]
