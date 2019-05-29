import os

from django.test import TestCase

from bills.algo.poc_detector import POCDetector
from bills.models import Bill
import cv2 as cv
from os import listdir
from os.path import isfile, join

base_dir = os.path.normpath(os.path.dirname(__file__) + "/../../test_set")
detector = il_bill = us_bill = None
def load_detector():
    global detector, il_bill, us_bill
    if detector is not None:
        return detector, us_bill, il_bill
    us_bill = Bill.objects.create(name="usd1", catalog="usd1", image_id="usd1", is_coin= False)
    il_bill = Bill.objects.create(name="il50", catalog="il50", image_id="il50", is_coin= False)
    detector = POCDetector(True)
    front = cv.imread(join(base_dir, "catalog", "us1", "front.jpg"))
    back = cv.imread(join(base_dir, "catalog", "us1", "back.jpg"))
    detector.add_bill_to_library(us_bill.id, front, back, us_bill)
    front = cv.imread(join(base_dir, "catalog", "il50", "front.jpg"))
    back = cv.imread(join(base_dir, "catalog", "il50", "back.jpg"))
    detector.add_bill_to_library(il_bill.id, front, back, il_bill)
    return detector, us_bill, il_bill


class POCTestCase(TestCase):
    def setUp(self):
        (_detector, _us_bill, _il_bill) = load_detector()
        self.detector = _detector
        self.us_bill = _us_bill
        self.il_bill = _il_bill

    def test_us1(self):
        match_us1 = list(listdir(join(base_dir, "us1")))
        for dir in match_us1:
            front_path = join(base_dir, "us1", dir, "front.jpg")
            back_path = join(base_dir, "us1", dir, "back.jpg")
            front = cv.imread(front_path)
            back = cv.imread(back_path)
            print("test us1 " + dir)
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
            print("test il50 " + dir)
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
            print("test no match " + dir)
            prediction = self.detector.predict(front, back)
            if prediction[0][1] >= 0.7:
                raise Exception("Match wrongly")

