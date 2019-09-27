import cv2 as cv
import numpy as np
import math

HSV_POSTIT_PINK = ('pink',156,155,198)
HSV_POSTIT_ORANGE = ('orange',17,147,214)

def heading(xy0,xy1):
    pass

def get_center(hsv_frame, hsv_color, width=5, render=False):
    lower = np.array((hsv_color[1]-width,128,50))
    upper = np.array((hsv_color[1]+width,255,255))
    mask = cv.inRange(hsv_frame, lower, upper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    if render:
        cv.imshow(hsv_color[0],mask)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours)>0):
        largest = max(contours, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(largest)
        M = cv.moments(largest)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return center
    else:
        return (None, None)

cap = cv.VideoCapture(0)
while(True):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of color in HSV

    try:
        centers = [get_center(hsv, c, render=True) for c in (HSV_POSTIT_PINK,HSV_POSTIT_ORANGE)]
        dy = centers[1][1]-centers[0][1]
        dx = centers[1][0]-centers[0][0]
        print('{0:.2f}'.format(math.atan(dy/dx)*360/(2*math.pi)),centers[0][0]-centers[1][0],centers[0][1]-centers[1][1])
    except Exception:
        heading = None

    cv.imshow('frame',frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
