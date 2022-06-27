import sys
from io import BytesIO
from django.conf import settings
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def crop_and_resize(image, size):
    uploaded_image = Image.open(image)
    filename = image.name
    origin_width, origin_height = uploaded_image.size
    resize_width, resize_height = size['length'], size['width']

    crop_width = origin_width if resize_width / resize_height >= origin_width / origin_height \
        else origin_height * resize_width / resize_height
    crop_height = origin_height if resize_width / resize_height <= origin_width / origin_height \
        else origin_width * resize_height / resize_width

    left = (origin_width - crop_width) / 2
    right = (origin_width + crop_width) / 2
    up = (origin_height - crop_height) / 2
    down = (origin_height + crop_height) / 2

    uploaded_image = uploaded_image.crop((left, up, right, down))
    uploaded_image = uploaded_image.resize(
        size=(size['length'], size['width'])
    )
    output = BytesIO()
    uploaded_image.save(output,
                        format=settings.PIL_FORMAT,
                        quality=settings.FILE_QUALITY)
    output.seek(0)
    cropped_image = InMemoryUploadedFile(
        output, 'ImageField',
        filename,
        settings.FILE_FORMAT,
        sys.getsizeof(output),
        None)

    return cropped_image
