import os

from django.core.management import BaseCommand

from bills.algo.detect_flow import DetectFlowImageSearch
from bills.algo.dummy import DummyAlgorithm
from bills.algo.hash import AverageHash, DHash, PHash, WDB4Hash, WHaarHash
from bills.models import Bill
from PIL import Image
import cv2 as cv


class Sandbox:

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def prepare(self):
        # get all bills
        # preprocess the library
        bills = Bill.objects.all()
        for bill in bills:
            front = bill.read_front_image()
            if front is None:
                print("ERROR: bill front image is empty " + str(bill.id))
                continue
            back = bill.read_back_image()
            self.algorithm.add_bill_to_library(bill.id, front, back, bill)

    def test(self, front_file, back_file):
        front = None
        back = None
        if front_file:
            front = cv.imread(front_file)
            if front is None:
                print("ERROR: Image is empty")
                return
        if back_file:
            back = cv.imread(back_file)

        prediction = self.algorithm.predict(front, back)
        print("for file ", front_file)
        for (bill_id, predict) in prediction:
            bill = Bill.objects.get(id=bill_id)
            print(predict * 100, "% ",bill.catalog, bill.name, bill.id)


class Command(BaseCommand):
    help = 'Run sandbox'

    def handle(self, *args, **options):
        base_dir = os.path.normpath(os.path.dirname(__file__) + "/../../../test_set")
        from os import listdir
        from os.path import isfile, join
        dirs = [f for f in listdir(base_dir) if not isfile(join(base_dir, f))]
        files_in_dirs = list(map(lambda d: [join(base_dir, d, f) for f in listdir(join(base_dir, d)) if isfile(join(base_dir, d, f))], dirs))
        flattened = [file for dir in files_in_dirs for file in dir]
        test_set = flattened
        # test_set = [
        #     base_dir + "/788/fr 788.jpg",
        #     base_dir + "/788/fr 788 d.jpg",
        #     base_dir + "/788/fr 788 f.jpg",
        #     base_dir + "/788/fr 788 j.jpg",
        #     base_dir + "/788/fr 788 o;.jpg",
        #     base_dir + "/788/fr 788 l.jpg"
        # ]
        #algos = [DummyAlgorithm(), AverageHash(), DHash(), PHash(), WHaarHash(), WDB4Hash()]
        algos = [DetectFlowImageSearch()]
        for algo in algos:
            sandbox = Sandbox(algo)
            print("build library")
            sandbox.prepare()
            for test_item in test_set:
                sandbox.test(test_item, None)

