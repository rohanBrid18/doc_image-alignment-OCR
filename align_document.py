import align_images
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image that we'll assign to template")
ap.add_argument("-t", "--template", required=True,
    help="path to input template image")
ap.add_argument("-d", "--debug", required=False,
    help="enter True to run in debug mode")
args = vars(ap.parse_args())

print("[Info] loading images...")
image = cv2.imread(args["image"])
template = cv2.imread(args["template"])

print("[Info] aligning images...")
aligned = align_images.align_images(image, template, debug=args["debug"])