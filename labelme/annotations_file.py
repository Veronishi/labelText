import base64
import contextlib
import io
import json
import os.path as osp

import PIL.Image

from labelme import __version__
from labelme.logger import logger
from labelme import PY2
from labelme import QT4
from labelme import utils


PIL.Image.MAX_IMAGE_PIXELS = None


@contextlib.contextmanager
def open(name, mode):
    assert mode in ["r", "w"]
    if PY2:
        mode += "b"
        encoding = None
    else:
        encoding = "utf-8"
    yield io.open(name, mode, encoding=encoding)
    return


class AnnotationFileError(Exception):
    pass


class AnnotationFile(object):

    suffix = ".json"

    def __init__(self, filename=None):
        self.shapes = []
        if filename is not None:
            self.load(filename)
        self.filename = filename

    def save(
        self,
        filename,
        shapes,
    ):
        try:
            with open(filename, "w") as f:
                json.dump(shapes, f, ensure_ascii=False, indent=4)
            self.filename = filename
        except Exception as e:
            raise AnnotationFileError(e)

    @staticmethod
    def is_label_file(filename):
        return osp.splitext(filename)[1].lower() == AnnotationFile.suffix
