from django.db.models import ImageField
from .utils import image_optimizer


class OptimizedImageField(ImageField):
    """An ImageField that gets optimized on save() using tinyPNG."""

    def save_form_data(self, instance, data):
        """Remove the OptimizedNotOptimized object on clearing the image."""
        # Are we updating an image?
        updating_image = (
            True if data and getattr(instance, self.name) != data else False
        )

        if updating_image:
            data = image_optimizer(
                data,
                self.optimized_image_output_size,
                self.optimized_image_resize_method,
            )

        super().save_form_data(instance, data)

    def __init__(
        self,
        optimized_image_output_size=None,
        optimized_image_resize_method=None,
        *args,
        **kwargs
    ):
        """
        Initialize OptimizedImageField instance.

        set up the `optimized_image_output_size` and
        `optimized_image_resize_method` arguments for the current
        `OptimizedImageField` instance.
        """
        # Set the optimized_image_output_size specified on your
        # OptimizedImageField model instances
        self.optimized_image_output_size = optimized_image_output_size

        # Set the optimized_image_resize_method specified on your
        # OptimizedImageField model instances
        self.optimized_image_resize_method = optimized_image_resize_method

        super().__init__(**kwargs)

    def deconstruct(self):
        """
        Deconstruct method.

        deconstruct the field, allowing us to handle the field data, useful
        in cases where you want to add optional arguments to your custom
        field but you need to exclude them from migrations.
        """
        name, path, args, kwargs = super().deconstruct()

        if kwargs.get("optimized_image_output_size"):
            del kwargs["optimized_image_output_size"]

        if kwargs.get("optimized_image_resize_method"):
            del kwargs["optimized_image_resize_method"]

        return name, path, args, kwargs
