import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        """
        Return a filename that's free on the target storage system,
        and availavle for new content toi be written to.

        Remove the file with the same name if exists
        """
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))

        return name