import os

from enum import Enum

class FileType(Enum):
    JSON = "json"
    YAML = "yaml"

def secure_delete(file, passes=5):
    with open(file, "ba+") as file:
        length = file.tell()
    with open(file, "br+") as file:
        for i in range(passes):
            file.seek(0)
            file.write(os.urandom(length))
    os.remove(file)