from django.db import models
from os import path
from jsonfield import JSONField
import cv2 as cv
import numpy as np

from bills.models.common import get_file_name, read_from_file_field


def get_catalog_file_name(instance, filename):
    return get_file_name("catalog")

class Bill(models.Model):
    name = models.CharField(max_length=50)
    catalog = models.CharField(max_length=30)
    front = models.ImageField(upload_to=get_catalog_file_name, blank= True)
    back = models.ImageField(upload_to=get_catalog_file_name, blank= True)
    pmg_link = models.CharField(max_length=256, blank= True)
    ebay_link = models.CharField(max_length=256, blank= True)
    heritage_link = models.CharField(max_length=256, blank= True)
    is_coin = models.BooleanField(default = False)
    image_id = models.CharField(max_length=256, blank= False)
    features = JSONField(default = {}, blank= True)

    def __str__(self):
        return self.name

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

