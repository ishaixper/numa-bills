import numpy as np
from bills.algo.base import ImageSearchAlgorithmBase

USD_CATALOG_ID = "usd1"
SHEKEL_ID = "il50"

class POCDetector(ImageSearchAlgorithmBase):

    def __init__(self):
        ImageSearchAlgorithmBase.__init__(self)
        self.USD_ID = 0
        self.IL_ID = 0

    def add_bill_to_library(self, id, front, back, bill):
        if bill.catalog == USD_CATALOG_ID:
            self.USD_ID = id
        elif bill.catalog == SHEKEL_ID:
            self.IL_ID = id

    def destroy(self):
        pass

    def predict(self, front=None, back=None):
        return [(self.USD_ID, .5), (self.IL_ID, .5)]

