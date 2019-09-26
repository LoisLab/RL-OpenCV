import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
while(True):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of color in HSV
    #lower = np.array((30,50,50))
    #upper = np.array((38,255,255))

    lower = np.array((5,50,50))
    upper = np.array((15,255,255))

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower, upper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if (len(contours)>0):
        largest = max(contours, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(largest)
        M = cv.moments(largest)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print(center)
    cv.imshow('mask',mask)
    cv.imshow('frame',frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
