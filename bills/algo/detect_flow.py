import cv2 as cv
import numpy as np
from bills.algo.base import ImageSearchAlgorithmBase
from bills.algo.coin_or_bill import detect_coin_or_bill
from bills.algo.keypoint_matcher import preapre_image_for_keypoints, get_keypoints, match_and_score


class DetectFlowImageSearch(ImageSearchAlgorithmBase):

    def __init__(self):
        self.catalog = list()

    def get_keypoints(self, img):
        img = preapre_image_for_keypoints(img)
        return get_keypoints(img)

    def get_match_and_score(self, a1, a2):
        return match_and_score(a1, a2)

    def add_bill_to_library(self, id, front, back, bill):
        coin_bill_detection = detect_coin_or_bill(front, back)
        if coin_bill_detection is None:
            print("could not calculate coin/bill for " + str(id))
        else:
            is_coin = coin_bill_detection[0] == "coin"
            if is_coin != bill.is_coin:
                print("detected WRONG coin/bill type for " + str(id))
        front_kp = self.get_keypoints(front)
        back_kp = None
        if back is not None:
            back_kp = self.get_keypoints(back)
        self.catalog.append({
            'id': id,
            'front': front,
            'back': back,
            'bill': bill,
            'front_kp': front_kp,
            'back_kp': back_kp,
        })

    def destroy(self):
        self.catalog = list()

    def predict(self, front=None, back=None):
        coin_bill_detection = detect_coin_or_bill(front, back)
        if coin_bill_detection is None:
            print("Not found shape")
            bills = self.catalog
        else:
            (type, shape) = coin_bill_detection
            print(type)
            if type == "coin":
                bills = list(filter(lambda b: b['bill'].is_coin, self.catalog))
            else:
                bills = list(filter(lambda b: not b['bill'].is_coin, self.catalog))

        (front_kp, front_des) = self.get_keypoints(front)
        back_kp = back_des = None
        if back is not None:
            (back_kp, back_des) = self.get_keypoints(back)
        dist = np.zeros((len(bills), 2))
        for i in range(len(bills)):
            bill = bills[i]
            (matching, distance) = self.get_match_and_score(bill['front_kp'], (front_kp, front_des))
            mean_distance = distance
            if bill['back_kp'] is not None and back_kp is not None:
                (matching, distance) = self.get_match_and_score(bill['back_kp'], (back_kp, back_des))
                mean_distance = (mean_distance + distance) / 2
            dist[i, 0] = bill["id"]
            dist[i, 1] = mean_distance

        sum = dist[:, 1].sum()
        dist[:, 1] = dist[:, 1] / sum
        dist = dist[dist[:,1].argsort()]
        dist[:, 1] = 1 - dist[:, 1]
        dist[:, 1] = np.power(dist[:, 1], 100)
        sum = dist[:, 1].sum()
        dist[:, 1] = dist[:, 1] / sum
        return dist
        # best_bill = dist[0, 0]
        # if not best_bill:
        #     raise Exception("did not match any bill")
        # image_id = best_bill['bill'].image_id
        # print(image_id)
        # id = best_bill['id']
        # p = min_distance / total_distance
        # return id, p