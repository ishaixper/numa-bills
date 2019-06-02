import numpy as np
from bills.algo.base import ImageSearchAlgorithmBase
from bills.algo.keypoint_matcher import preapre_image_for_keypoints, get_keypoints, match_and_score
from os import path
import cv2 as cv

USD_CATALOG_ID = "usd1"
SHEKEL_ID = "il50"

class POCDetector(ImageSearchAlgorithmBase):

    def __init__(self, debug = False):
        ImageSearchAlgorithmBase.__init__(self, debug)
        self.USD_ID = 0
        self.IL_ID = 0
        self.us_keypoints = None
        self.il_keypoints = None
        self.threshold = {'us': 150, 'il': 130}
        self.shift = {'us': 0, 'il': 0}
        # lena = cv.imread(path.join(path.dirname(__file__), "..", "..", "test_set", "catalog","lena.jpg"))
        # self.lena_kp = self.get_keypoints(lena)


    def get_keypoints(self, img):
        img = preapre_image_for_keypoints(img)
        return get_keypoints(img)

    def add_bill_to_library(self, id, front, back, bill):
        if bill.catalog == USD_CATALOG_ID:
            self.USD_ID = id
            self.us_keypoints = (self.get_keypoints(front), self.get_keypoints(back))
        elif bill.catalog == SHEKEL_ID:
            self.IL_ID = id
            self.il_keypoints = (self.get_keypoints(front), self.get_keypoints(back))

    def destroy(self):
        pass

    def create_distribution_from_scores(self, scores):
        values = np.array(list(scores.values()))
        # values = np.exp(values / 50)
        values = np.exp(values * 2)
        sum = np.sum(values)
        values = values / sum
        return values

    def predict(self, front=None, back=None):
        if self.USD_ID == 0 or self.IL_ID == 0:
            raise Exception("Did not load notes")
        candidates = {"us": self.us_keypoints, "il": self.il_keypoints}
        scores = {}
        relative = {}
        front_kp = self.get_keypoints(front)
        back_kp = self.get_keypoints(back)
        max_score = -float("inf")
        min_matching = None
        min_type = None
        min_score = float("inf")
        total_scores = 0
        for (name, candidate_kp) in candidates.items():
            (cat_front_kp, cat_back_kp) = candidate_kp
            (matching_front, distance_front) = match_and_score(cat_front_kp, front_kp)
            (matching_back, distance_back) = match_and_score(cat_back_kp, back_kp)
            print(name, distance_front, distance_back)
            # front_score = distance_front / cat_front_distance
            # back_score = distance_back / cat_back_distance
            score = np.mean([distance_front, distance_back])
            scores[name] = -score - self.shift[name]
            relative[name] = (-score - self.shift[name])/ self.threshold[name]

        if self.debug:
            print(scores)
            print(relative)
        p = self.create_distribution_from_scores(relative)
        if self.debug:
            print(p)
        score_delta = abs(relative['us'] - relative['il'])
        if score_delta < 0.1:
            print("too close, can't match")
            return ((self.USD_ID, 0.5), (self.IL_ID, 0.5))
        best_rate = max(relative['us'], relative['il'])
        print("best", best_rate)
        if best_rate < -1.4:
            print("too far from either")
            return ((self.USD_ID, 0.5), (self.IL_ID, 0.5))

        # if relative['us'] < relative['il']:
        #     if relative['us'] > 1:
        #         print("too far from either")
        #         return ((self.USD_ID, 0.5), (self.IL_ID, 0.5))
        #     else:
        #         return ((self.USD_ID, 1.0), (self.IL_ID, 0.0))
        # else:
        #     if relative['il'] > 1:
        #         print("too far from either")
        #         return ((self.USD_ID, 0.5), (self.IL_ID, 0.5))
        #     else:
        #         return ((self.IL_ID, 1.0), (self.USD_ID, 0.0))
        results = np.zeros((2, 2))
        results[:, 0] = [self.USD_ID, self.IL_ID]
        results[:, 1] = p
        results = results[results[:,1].argsort()[::-1]]
        return results

