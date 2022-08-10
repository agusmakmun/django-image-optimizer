from django.shortcuts import render
from io import BytesIO
from PIL import Image
from uuid import uuid4

from .forms import PostForm
from .models import Post


# from ...image_optimizer.utils import crop_image_on_axis
# Create your views here.
def upload(request):
    posts = Post.objects.all()
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form = form.save(commit=False)
            photo = request.FILES.get("photo")
            width = int(request.POST.get("width"))
            height = int(request.POST.get("height"))
            x = float(request.POST.get("x"))
            y = float(request.POST.get("y"))
            extension = photo.content_type.split('/')[1]
            photo = crop_image_on_axis(photo, width, height, x, y, extension)
            form.photo = photo
            form.save()
    form = PostForm()
    return render(request, template_name="upload.html", context={"form" : form, "posts" : posts})

''' Tested with Pillow. '''
def crop_image_on_axis(image, width, height, x, y, extension):

    '''Open the passed image'''
    img = Image.open(image)

    '''Initialise bytes io'''
    bytes_io = BytesIO()

    '''crop the image through axis'''
    img = img.crop((x, y, width+x, height+y))

    '''resize the image and optimise it for file size, making smaller as possible'''
    img = img.resize((width, height), Image.ANTIALIAS)

    ''' This line is optional, for safe side, image name should be unique.'''
    img.name = "{}.{}".format(uuid4().hex, extension)

    ''' If the file extension is JPEG, convert the output_image to RGB'''
    if extension == 'JPEG':
        img = image.convert('RGB')
    img.save(bytes_io, format=extension, optimize=True)

    '''return the image'''
    image.seek(0)

    ''' Write back new image'''
    image.file.write(bytes_io.getvalue())

    '''truncate the file size.'''
    image.file.truncate()
    return image
