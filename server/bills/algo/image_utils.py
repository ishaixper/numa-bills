import cv2 as cv

def scale_down(img, max_width, max_height):
    # scale down
    width = img.shape[0]
    height = img.shape[1]
    scale_width = max_width / width
    scale_height = max_height / height
    scale = min(max(scale_height, scale_width), 1)
    return cv.resize(img, (0, 0), fx=scale, fy=scale)