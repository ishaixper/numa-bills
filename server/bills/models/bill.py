from django.db import models
from os import path
from jsonfield import JSONField
import cv2 as cv
import numpy as np

UPLOAD_DIR = path.normpath("./uploads/bills")

class Bill(models.Model):
    name = models.CharField(max_length=50)
    catalog = models.CharField(max_length=30)
    front = models.ImageField(upload_to=UPLOAD_DIR, blank= True)
    back = models.ImageField(upload_to=UPLOAD_DIR, blank= True)
    pmg_link = models.CharField(max_length=256, blank= True)
    ebay_link = models.CharField(max_length=256, blank= True)
    heritage_link = models.CharField(max_length=256, blank= True)
    is_coin = models.BooleanField(default = False)
    image_id = models.CharField(max_length=256, blank= False)
    features = JSONField(default = {}, blank= True)

    def __str__(self):
        return self.name

    def read_from_file_stream(self, file_field):
        file_stream = file_field.open('rb')
        img_array = np.asarray(bytearray(file_stream.read()), dtype=np.uint8)
        return cv.imdecode(img_array, 0)

    def read_front_image(self):
        try:
            return self.read_from_file_stream(self.front)
        except Exception as e:
            print("error loading ", e)
            return None
        #return Image.open(self.front)

    def read_back_image(self):
        if not self.back:
            return None
        return self.read_from_file_stream(self.back)
#        return Image.open(self.back)

