from urllib.parse import urlparse
from rest_framework.serializers import ValidationError


class MaterialsValidators:

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value:
            parsed_url = urlparse(value)
            if parsed_url.netloc not in ['www.youtube.com', 'youtube.com', 'youtu.be']:
                raise ValidationError({self.field: 'Разрешены только ссылки на видео с YouTube.'})
