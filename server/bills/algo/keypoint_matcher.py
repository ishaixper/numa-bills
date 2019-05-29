import cv2 as cv
import numpy as np

from bills.algo.image_utils import scale_down

NUM_KEYPOINTS = 2000
HOMOGRAPHY_METHOD = cv.RANSAC
RANSAC_REPROJ_THRESHOLD = 4.0

orb_detector = cv.ORB_create(NUM_KEYPOINTS, patchSize=41, edgeThreshold=55)
# create BFMatcher object
bf_matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

def preapre_image_for_keypoints(img):
    return scale_down(img, 550, 550)

def get_keypoints(front):
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb_detector.detectAndCompute(front, mask=None)
    return kp1, des1

def match_and_score(a1, a2, debug = False):
    (kp1, des1) = a1
    (kp2, des2) = a2
    matches = bf_matcher.match(des1, des2)
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    H, mask = cv.findHomography(src_pts, dst_pts, HOMOGRAPHY_METHOD, RANSAC_REPROJ_THRESHOLD)
    computed_pt = cv.perspectiveTransform(src_pts, H)
    x_delta = computed_pt[:, 0, 0] - dst_pts[:, 0, 0]
    y_delta = computed_pt[:, 0, 1] - dst_pts[:, 0, 1]
    error_pt = np.sqrt(x_delta * x_delta + y_delta * y_delta).sum() / len(src_pts)
    return (matches, H, mask), error_pt


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    catalog_front = preapre_image_for_keypoints(cv.imread("../../uploads/FR_788_front_pQ9pAh8.jpg"))
    #test_front = preapre_image(cv.imread("../../test_set/788/fr 788.jpg"))
    test_front = preapre_image_for_keypoints(cv.imread("../../test_set/fr 748/fr 748 back.jpg"))

    keypoints1 = get_keypoints(catalog_front)
    keypoints2 = get_keypoints(test_front)
    (kp1, des1) = keypoints1
    (kp2, des2) = keypoints2
    u1 = cv.bitwise_and(catalog_front, catalog_front, mask=None)
    u2 = cv.bitwise_and(test_front, test_front, mask=None)
    for kp in kp1:
        cv.circle(u1, (int(kp.pt[0]), int(kp.pt[1])), 7, (0, 0, 255), -1)
    for kp in kp2:
        cv.circle(u2, (int(kp.pt[0]), int(kp.pt[1])), 7, (0, 0, 255), -1)
    print('kp1')
    plt.imshow(u1)
    plt.show()
    print('kp2')
    plt.imshow(u2)
    plt.show()
    (matches, H, mask), distance = match_and_score(keypoints1, keypoints2, True)
    print("Distance", distance)
    print('aligned image:')
    plt.imshow(test_front)
    plt.show()

