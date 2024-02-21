from os import path

import cv2
import cv2 as cv
from matplotlib import pyplot as plt

my_dir = path.dirname(__file__)
mask_file = path.join(my_dir, 'data', 'mask.bmp')
camera_file = path.join(my_dir, 'data', 'image_left.bmp')


mask_img = cv.imread(mask_file, cv.IMREAD_GRAYSCALE)
cam_img = cv.imread(camera_file, cv.IMREAD_GRAYSCALE)

# Initiate ORB detector
orb = cv.ORB_create()
# find the keypoints with ORB
mask_kp, mask_descr = orb.detectAndCompute(mask_img, None)
cam_kp, cam_descr = orb.detectAndCompute(cam_img, None)

matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
matches = matcher.match(mask_descr, cam_descr)

final_img = cv.drawMatches(mask_img,
                           mask_kp,
                           cam_img,
                           cam_kp,
                           matches,
                           None)

cv2.imshow("Matchink Keypoints", final_img)

cv2.waitKey()
