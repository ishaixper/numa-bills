import cv2
import numpy
from django.db import models
from PIL import Image
from os import path

UPLOAD_DIR = path.normpath(path.dirname(__file__) + "/../uploads")

class Bill(models.Model):
    name = models.CharField(max_length=50)
    catalog = models.CharField(max_length=30)
    front = models.ImageField(upload_to=UPLOAD_DIR)
    back = models.ImageField(upload_to=UPLOAD_DIR)
    pmg_link = models.CharField(max_length=256, blank= True)
    ebay_link = models.CharField(max_length=256, blank= True)
    heritage_link = models.CharField(max_length=256, blank= True)

    def __str__(self):
        return self.name

    def read_front_image(self):
        if not self.front.url:
            return None
        return Image.open(self.front)

    def read_back_image(self):
        if not self.back.url:
            return None
        return Image.open(self.back)
