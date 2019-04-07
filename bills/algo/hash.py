import imagehash
import numpy as np

from bills.algo.base import ImageSearchAlgorithmBase

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

class HashBase(ImageSearchAlgorithmBase):
    def __init__(self, hashfunc):
        ImageSearchAlgorithmBase.__init__(self)
        self.hashfunc = hashfunc
        self.bills = []
        #
        # if hashmethod == 'ahash':
        #     hashfunc = imagehash.average_hash
        # elif hashmethod == 'phash':
        #     hashfunc = imagehash.phash
        # elif hashmethod == 'dhash':
        #     hashfunc = imagehash.dhash
        # elif hashmethod == 'whash-haar':
        #     hashfunc = imagehash.whash
        # elif hashmethod == 'whash-db4':
        #     hashfunc = lambda img: imagehash.whash(img, mode='db4')

    def add_bill_to_library(self, id, front, back):
        item = (id, self.hashfunc(front))
        self.bills.append(item)

    def destroy(self):
        self.bills = []

    def predict(self, front=None, back=None):
        N = len(self.bills)
        this_hash = self.hashfunc(front)
        distances = list(map(lambda pair: abs(this_hash - pair[1]), self.bills))
        print(distances)
        distances = 1 - softmax(distances)
        mat = np.zeros(shape=(N, 2))
        mat[:, 1] = distances
        mat[:, 0] = list(map(lambda pair: pair[0], self.bills))
        mat.sort(axis=1)
        mat = np.flip(mat, axis=1)
        return mat

class AverageHash(HashBase):
    def __init__(self):
        HashBase.__init__(self, imagehash.average_hash)

class PHash(HashBase):
    def __init__(self):
        HashBase.__init__(self, imagehash.phash)

class DHash(HashBase):
    def __init__(self):
        HashBase.__init__(self, imagehash.dhash)

class WHaarHash(HashBase):
    def __init__(self):
        HashBase.__init__(self, imagehash.whash)

class WDB4Hash(HashBase):
    def __init__(self):
        HashBase.__init__(self, lambda img: imagehash.whash(img, mode='db4'))


