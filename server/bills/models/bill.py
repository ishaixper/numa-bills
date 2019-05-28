from django.db import models
from os import path
from jsonfield import JSONField
import cv2 as cv

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

    def read_front_image(self):
        try:
            if not self.front.url:
                return None
            return cv.imread(self.front.path)
        except:
            print("error loading ")
            return None
        #return Image.open(self.front)

    def read_back_image(self):
        if not self.back.url:
            return None
        return cv.imread(self.front.path)
#        return Image.open(self.back)
