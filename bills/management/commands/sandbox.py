import os

from django.core.management import BaseCommand

from bills.algo.dummy import DummyAlgorithm
from bills.algo.hash import AverageHash, DHash, PHash, WDB4Hash, WHaarHash
from bills.models import Bill
from PIL import Image


class Sandbox:

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def prepare(self):
        # get all bills
        # preprocess the library
        bills = Bill.objects.all()
        for bill in bills:
            front = bill.read_front_image()
            back = bill.read_back_image()

            self.algorithm.add_bill_to_library(bill.id, front, back)

    def test(self, front_file, back_file):
        front = None
        back = None
        if front_file:
            front = Image.open(front_file)
        if back_file:
            back = Image.open(back_file)

        prediction = self.algorithm.predict(front, back)

        for (bill_id, predict) in prediction:
            bill = Bill.objects.get(id=bill_id)
            print(predict * 100, "% ", bill.name)


class Command(BaseCommand):
    help = 'Run sandbox'

    def handle(self, *args, **options):
        base_dir = os.path.normpath(os.path.dirname(__file__) + "/../../../test_set")
        test_set = [
            base_dir + "/788/fr 788.jpg",
            base_dir + "/788/fr 788 d.jpg",
            base_dir + "/788/fr 788 f.jpg",
            base_dir + "/788/fr 788 j.jpg",
            base_dir + "/788/fr 788 o;.jpg",
            base_dir + "/788/fr 788 l.jpg"
        ]
        algos = [DummyAlgorithm(), AverageHash(), DHash(), PHash(), WHaarHash(), WDB4Hash()]
        for algo in algos:
            sandbox = Sandbox(algo)
            print("build library")
            sandbox.prepare()
            for test_item in test_set:
                sandbox.test(test_item, None)

