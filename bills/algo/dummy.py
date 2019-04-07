from bills.algo.base import ImageSearchAlgorithmBase


class DummyAlgorithm(ImageSearchAlgorithmBase):

    def __init__(self):
        ImageSearchAlgorithmBase.__init__(self)
        self.bills = []

    def add_bill_to_library(self, id, front, back):
        self.bills.append(id)

    def destroy(self):
        self.bills = []

    def predict(self, front=None, back=None):
        arr = []
        length = len(self.bills)
        p = 1 / length
        for bill in self.bills:
            arr.append((bill, p))
        return arr
