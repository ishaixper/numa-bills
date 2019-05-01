import cv2 as cv
import numpy as np
from bills.algo.base import ImageSearchAlgorithmBase
from bills.algo.coin_or_bill import detect_coin_or_bill

NUM_KEYPOINTS = 50
HOMOGRAPHY_METHOD = cv.RANSAC
RANSAC_REPROJ_THRESHOLD = 4.0

class DetectFlowImageSearch(ImageSearchAlgorithmBase):

    def __init__(self):
        self.catalog = list()
        self.orb_detector = cv.ORB_create(NUM_KEYPOINTS, patchSize=120, edgeThreshold=120)
        # create BFMatcher object
        self.bf_matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    def get_keypoints(self, front):
        # find the keypoints and descriptors with ORB
        kp1, des1 = self.orb_detector.detectAndCompute(front)
        return kp1, des1

    def get_match_and_score(self, a1, a2):
        (kp1, des1) = a1
        (kp2, des2) = a2
        matches = self.bf_matcher.match(des1, des2)
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        H, mask = cv.findHomography(src_pts, dst_pts, HOMOGRAPHY_METHOD, RANSAC_REPROJ_THRESHOLD)
        computed_pt = H * src_pts
        error_pt = np.sqrt((computed_pt.x - dst_pts.x) * (computed_pt.x - dst_pts.x) + (computed_pt.y - dst_pts.y) * (
                    computed_pt.y - dst_pts.y))
        return (matches, H, mask), error_pt

    def add_bill_to_library(self, id, front, back, bill):
        coin_bill_detection = detect_coin_or_bill(front, back)
        if coin_bill_detection == None:
            print("could not calculate coin/bill for " + id)
        else:
            is_coin = coin_bill_detection[0] == "coin"
            if is_coin != bill.is_coin:
                print("detected WRONG coin/bill type for " + id)

        front_kp = self.get_keypoints(front)
        back_kp = None
        if back:
            back_kp = self.get_keypoints(back)
        self.catalog.append({
            'id': id,
            'front': front,
            'back': back,
            'bill': bill,
            'front_kp': front_kp,
            'back_kp': back_kp})

    def destroy(self):
        self.catalog = list()

    def predict(self, front=None, back=None):
        coin_bill_detection = detect_coin_or_bill(front, back)
        if coin_bill_detection == None:
            return "Not found"
        (type, shape) = coin_bill_detection
        print(type)
        if type == "coin":
            bills = filter(lambda b: b.is_coin, self.catalog)
        else:
            bills = filter(lambda b: not b.is_coin, self.catalog)

        (front_kp, front_des) = self.get_keypoints(front)
        back_kp = back_des = None
        if back:
            (back_kp, back_des) = self.get_keypoints(back)
        min_distance = float('inf')
        best_matching = None
        best_bill = None
        for bill in bills:
            (matching, distance) = self.get_match_and_score(bill.front_kp, (front_kp, front_des))
            if distance < min_distance:
                min_distance = distance
                best_matching = matching
                best_bill = bill
            if bill.back_kp and back_kp:
                (matching, distance) = self.get_match_and_score(bill.back_kp, (back_kp, back_des))
                if distance < min_distance:
                    min_distance = distance
                    best_matching = matching
                    best_bill = bill

        if not best_bill:
            raise Exception("did not match any bill")
        image_id = best_bill.image_id
        print(image_id)
