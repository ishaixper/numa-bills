import cv2
import numpy as np
from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter

font = cv2.FONT_HERSHEY_COMPLEX


def find_shape_hough(img, debug=False, debug_name=""):
    edges = canny(img, sigma=2.0,
                  low_threshold=0.55, high_threshold=0.8)

    # Perform a Hough Transform
    # The accuracy corresponds to the bin size of a major axis.
    # The value is chosen in order to get a single high accumulator.
    # The threshold eliminates low accumulators
    result = hough_ellipse(edges, accuracy=20, threshold=250,
                           min_size=100, max_size=120)
    result.sort(order='accumulator')
    found = len(result)
    if found == 0:
        return (0, 0, None)
    best = list(result[-1])
    yc, xc, a, b = [int(round(x)) for x in best[1:5]]
    orientation = best[5]
    # Draw the ellipse on the original image
    cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
    img[cy, cx] = (0, 0, 255)
    return (found, 14, None)


def find_single_external_shape(img, debug=False, debug_name=""):
    (width, height) = img.shape
    contours, hir = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if debug:
        blank_image = np.zeros(img.shape, np.uint8)
        blank_image = 255 - blank_image
    found = 0
    points = 0
    box = None
    flatten = None
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        points = len(approx)
        if points < 4:
            continue
        # skip shapes that are less than 20% of width or height
        (n, _, _) = approx.shape
        flatten = approx.reshape(n, 2)
        x_col = flatten[:, 0]
        y_col = flatten[:, 1]
        xmax = x_col.max()
        ymax = y_col.max()
        xmin = x_col.min()
        ymin = y_col.min()
        x_delta = xmax - xmin
        y_delta = ymax - ymin

        print(xmax, ymax, xmin, ymin)
        if x_delta < width / 20 or y_delta < height / 20:
            continue
        box = (xmin, ymin, xmax, ymax)
        found += 1
        if debug:
            cv2.drawContours(blank_image, [approx], 0, (23), 5)
            points = len(approx)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            print(len(approx))
            if len(approx) == 4:
                cv2.putText(blank_image, "Rectangle", (x, y), font, 1, (14))
            elif len(approx) == 5:
                cv2.putText(blank_image, "Pentagon", (x, y), font, 1, (152))
            elif 6 < len(approx) < 15:
                cv2.putText(blank_image, "Ellipse", (x, y), font, 1, (234))
            else:
                cv2.putText(blank_image, "Circle", (x, y), font, 1, (12))
    if debug:
        cv2.imshow(str(debug_name), np.hstack((img, blank_image)))
    return (found, points, box, flatten)

def is_shape_roind(approx, points):
    degrees = list()
    for i in range(points):
        trio = (approx[i], approx[(i + 1) % points], approx[(i + 2) % points])
        ba = trio[0] - trio[1]
        bc = trio[2] - trio[1]
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        degree = np.degrees(angle)
        degrees.append(degree)
    for i in range(points):
        #print(degrees[i])
        if degrees[i] < 90:
            return False
        delta = degrees[(i + 1) % points] - degrees[i]
        if delta > 90:
            return False
    print("round")
    print(degrees)
    return True

def detect_coin_or_bill(front, back, debug = False):
    img = front
    # scale down
    (width, height) = img.shape
    scale_width = 250 / width
    scale_height = 250 / height
    scale = min(max(scale_height, scale_width), 1)
    img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    stack = img
    (width, height) = img.shape

    # inverse, background should be black
    # img = 255 - img

    # smooth image
    kernel = np.ones((5, 5), np.float32) / 25
    img = cv2.filter2D(img, -1, kernel)

    # equalize historgram
    img = cv2.equalizeHist(img)
    if debug:
        stack = np.hstack((stack, img))

    # kernel = np.ones((10, 10), np.uint8)
    # cv2.dilate(img, kernel, iterations=1)
    # kernel = np.ones((10, 10), np.uint8)
    # cv2.erode(img, kernel, iterations=1)

    for th in range(50, 255, 15):
        _, th_img = cv2.threshold(img, th, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        (found, points, box, approx) = find_single_external_shape(th_img, debug, th)
        # import matplotlib.pyplot as plt
        # plt.plot(approx)
        # plt.ylabel('some numbers')
        # plt.show()
        # (found, points, box) = find_shape_hough(th_img, True, th)
        print(found, points)
        if found == 1:
            print("found single shape")
            if points == 4:
                print("rect")
                return ("bill", approx)
            if points > 6:
                if is_shape_roind(approx, points):
                    return ("coin", approx)
                for i in range(points):
                    exclude = list(approx)
                    del exclude[i]
                    if is_shape_roind(exclude, points - 1):
                        return ("coin",approx)
                return None
                # cv2.imshow("dst", img)
    # # cv2.imshow("Threshold", threshold)


if __name__ == "__main__":
    img = cv2.imread("bill.jpg", cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread("coin1.jpg", cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread("coin-down.jpg", cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread("duck.jpg", cv2.IMREAD_GRAYSCALE)
    answer = detect_coin_or_bill(img, None, True)
    print(answer)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
