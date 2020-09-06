import numpy as np
import imutils
import cv2

def align_images(image, template, maxFeatures=500, keepPercent=0.2, debug=False):
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)