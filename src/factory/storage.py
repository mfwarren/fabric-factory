import os
import uuid
from django.core.files.storage import FileSystemStorage


class FileSystemStorageUuidName(FileSystemStorage):
    def get_available_name(self, name):
        """
        Returns a filename composed of a uuid on the target storage system.
        """
        root, file_ext = os.path.splitext(name)
        unique_id = uuid.uuid1()
        name = '%s_%s%s' % (root, unique_id, file_ext)
        return name
