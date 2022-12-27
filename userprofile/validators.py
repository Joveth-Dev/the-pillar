from django.core.exceptions import ValidationError


def validate_image_size(file):
    max_size_mb = 1

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Image cannot be larger than {max_size_mb}MB')
