from django.db import models
from os import path
from jsonfield import JSONField
import cv2 as cv
from bills.models.common import get_file_name, read_from_file_field


def get_detection_file_name(instance, filename):
    return get_file_name("detection")

class Detection(models.Model):
    front = models.ImageField(upload_to=get_detection_file_name)
    back = models.ImageField(upload_to=get_detection_file_name)
    created_on = models.DateTimeField(auto_now_add=True)
    time = models.IntegerField(default=0)
    result = JSONField(default=[])

    def __str__(self):
        return str(self.result)

    def read_front_image(self):
        try:
            return read_from_file_field(self.front)
        except Exception as e:
            print("error loading ", e)
            return None
        #return Image.open(self.front)

    def read_back_image(self):
        if not self.back:
            return None
        return read_from_file_field(self.back)
#        return Image.open(self.back)
