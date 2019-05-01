from abc import abstractmethod, ABC

from bills.models import Bill

'''
Base class for Image Search Algorithm
'''
class ImageSearchAlgorithmBase(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def add_bill_to_library(self, id, front, back, bill):
        pass

    @abstractmethod
    def destroy(self):
        pass

    '''
    Recevies image (cv) represtantions of front and back
    Returns an array of tuples. Each tuple has bill id and prediction score.
    Array is ordered by highest prediction
    '''
    @abstractmethod
    def predict(self, front=None, back=None):
        pass
