from django.db import models
from os import path
from jsonfield import JSONField
import cv2 as cv

UPLOAD_DIR = path.normpath("./uploads/detections")

class Detection(models.Model):
    front = models.ImageField(upload_to=UPLOAD_DIR)
    back = models.ImageField(upload_to=UPLOAD_DIR)

    def __str__(self):
        return self.name

    def read_front_image(self):
        if not self.front.url:
            return None
        return cv.imread(self.front.path)
        #return Image.open(self.front)

    def read_back_image(self):
        if not self.back.url:
            return None
        return cv.imread(self.front.path)
#        return Image.open(self.back)
