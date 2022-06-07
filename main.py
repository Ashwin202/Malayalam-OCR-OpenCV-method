import numpy as np
import argparse
import imutils
from imutils.contours import sort_contours
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

# load the input image from disk, convert it to grayscale, and blur
# it to reduce noise
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)


# perform edge detection, find contours in the edge map, and sort the
# resulting contours from left-to-right
edged = cv2.Canny(blurred, 30, 150)  # increases breaking
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_NONE)

cnts = imutils.grab_contours(cnts)
cnts = sort_contours(cnts, method="left-to-right")[0]
# initialize the list of contour bounding boxes and associated
# characters that we'll be OCR'ing
chars = []

# loop over the contours
for c in cnts:
    area = cv2.contourArea(c)

    if area < 50:
        img1 = cv2.drawContours(image, c, -1, (255, 0, 0), 1)
        peri = cv2.arcLength(c, True)
        print("Area= ", area)
        print("perimeter", peri)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        obj = len(approx)
        x, y, w, h = cv2.boundingRect(approx)

        cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 1)


cv2.imshow("Image", img1)
cv2.waitKey(0)

#     # compute the bounding box of the contour
#     (x, y, w, h) = cv2.boundingRect(c)

#     # filter out bounding boxes, ensuring they are neither too small
#     # nor too large

#     # if (w >= 5 and w <= 150) and (h >= 15 and h <= 120):
#     if (w >= 25 and w <= 150) and (h >= 20 and h <= 120):
#         # extract the character and threshold it to make the character
#         # appear as *white* (foreground) on a *black* background, then
#         # grab the width and height of the thresholded image
#         roi = gray[y:y + h, x:x + w]
#         thresh = cv2.threshold(
#             roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#         (tH, tW) = thresh.shape
#         if tW > tH:
#             thresh = imutils.resize(thresh, width=32)

#         # otherwise, resize along the height
#         else:
#             thresh = imutils.resize(thresh, height=32)

#         # re-grab the image dimensions (now that its been resized)
#         # and then determine how much we need to pad the width and
#         # height such that our image will be 32x32
#         (tH, tW) = thresh.shape
#         dX = int(max(0, 32 - tW) / 2.0)
#         dY = int(max(0, 32 - tH) / 2.0)

#         # pad the image and force 32x32 dimensions
#         padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
#                                     left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
#                                     value=(0, 0, 0))
#         padded = cv2.resize(padded, (32, 32))

#         # update our list of characters that will be OCR'd
#         chars.append((padded, (x, y, w, h)))
#         # cv2.imshow("Image", image)
#         # cv2.waitKey(0)

# # extract the bounding box locations and padded characters
# boxes = [b[1] for b in chars]
# chars = np.array([c[0] for c in chars], dtype="float32")
# counts = [i for i in range(len(boxes))]


# # # # # # # loop over the predictions and bounding box locations together
# for (pred, (x, y, w, h)) in zip(counts, boxes):
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
# cv2.imshow("Image", image)
# cv2.waitKey(0)
