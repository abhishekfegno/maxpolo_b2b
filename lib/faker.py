import os

from django.conf import settings
from django.templatetags.static import static


class FakeImage:
    def __init__(self, instance=None):
        # self.gender = 'M'
        if instance:
            self.photo = instance.photo.url

    @property
    def name(self):
        print(settings.DEFAULT_IMAGE)

        if not self.photo:
            return settings.DEFAULT_IMAGE
        return self.photo.url

    @property
    def url(self):
        return static(self.name)

    @property
    def path(self):
        return os.path.join(settings.BASE_DIR, 'public', 'assets', self.name)
