import os
from hyrodactil.settings.base import MEDIA_ROOT


def save_file(file):
    new_file_name = os.path.join(MEDIA_ROOT, file.name)

    destination = open(new_file_name, 'wb+')
    destination.write(file.read())
    destination.close()

    return str(new_file_name)
