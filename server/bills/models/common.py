import uuid
from os import path
import numpy as np
import cv2 as cv


is_test = False

def set_storage_test(test):
    global is_test
    is_test = test

def get_file_name(group):
    name = "%s.%s" % (uuid.uuid4(), "jpg")
    dir = path.normpath("/app/uploads/" + group)
    if is_test:
        return path.join("test", dir, name)
    else:
        return path.join(dir, name)

def read_from_file_field(file_field):
    return read_from_file_stream(file_field.open('rb'))

def read_from_file_stream(file_stream):
    img_array = np.asarray(bytearray(file_stream.read()), dtype=np.uint8)
    return cv.imdecode(img_array, 0)
