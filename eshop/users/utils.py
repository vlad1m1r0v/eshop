import sys
from io import BytesIO
from django.conf import settings
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def crop_and_resize(image):
    uploaded_image = Image.open(image)
    filename = image.name
    origin_width, origin_height = uploaded_image.size
    left = (origin_width - origin_height) / 2 if origin_width > origin_height else 0
    right = origin_height + (origin_width - origin_height) / 2 if origin_width > origin_height else origin_width
    up = (origin_height - origin_width) / 2 if origin_height > origin_width else 0
    down = origin_width + (origin_height - origin_width) / 2 if origin_height > origin_width else origin_height
    uploaded_image = uploaded_image.crop((left, up, right, down))
    uploaded_image = uploaded_image.resize(
        size=(settings.AVATAR_SIZE, settings.AVATAR_SIZE)
    )
    output = BytesIO()
    uploaded_image.save(output,
                        format=settings.AVATAR_PIL_FORMAT,
                        quality=settings.AVATAR_QUALITY)
    output.seek(0)
    cropped_image = InMemoryUploadedFile(
        output, 'ImageField',
        filename,
        settings.AVATAR_FILE_FORMAT,
        sys.getsizeof(output),
        None)
    return cropped_image
