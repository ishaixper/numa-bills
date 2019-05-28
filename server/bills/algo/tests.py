import os

from django.test import override_settings, testcases, TestCase

from bills.algo.poc_detector import POCDetector
from bills.models import Bill
import cv2 as cv
from os import listdir
from os.path import isfile, join

base_dir = os.path.normpath(os.path.dirname(__file__) + "/../../test_set")


class POCTestCase(TestCase):
    def setUp(self):
        self.us_bill = Bill.objects.create(name="usd1", catalog="usd1", image_id="usd1", is_coin= False)
        self.il_bill = Bill.objects.create(name="il50", catalog="il50", image_id="il50", is_coin= False)
        self.detector = POCDetector()
        self.detector.add_bill_to_library(self.us_bill.id, None, None, self.us_bill)
        self.detector.add_bill_to_library(self.il_bill.id, None, None, self.il_bill)

    def test_us1(self):
        match_us1 = list(listdir(join(base_dir, "us1")))
        for dir in match_us1:
            front_path = join(base_dir, "us1", dir, "front.jpg")
            back_path = join(base_dir, "us1", dir, "back.jpg")
            front = cv.imread(front_path)
            back = cv.imread(back_path)
            prediction = self.detector.predict(front, back)
            if prediction[0][1] < 0.7:
                raise Exception("Did not match us1")
            if prediction[0][0] != self.us_bill.id:
                raise Exception("matched IL instead of US")

    def test_il50(self):
        match_us1 = list(listdir(join(base_dir, "il50")))
        for dir in match_us1:
            front_path = join(base_dir, "il50", dir, "front.jpg")
            back_path = join(base_dir, "il50", dir, "back.jpg")
            front = cv.imread(front_path)
            back = cv.imread(back_path)
            prediction = self.detector.predict(front, back)
            if prediction[0][1] < 0.7:
                raise Exception("Did not match")
            if prediction[0][0] != self.il_bill.id:
                raise Exception("matched US instead of IL")

    def test_no_match(self):
        match_us1 = list(listdir(join(base_dir, "no_match")))
        for dir in match_us1:
            front_path = join(base_dir, "no_match", dir, "front.jpg")
            back_path = join(base_dir, "no_match", dir, "back.jpg")
            front = cv.imread(front_path)
            back = cv.imread(back_path)
            prediction = self.detector.predict(front, back)
            if prediction[0][1] >= 0.7:
                raise Exception("Match wrongly")

