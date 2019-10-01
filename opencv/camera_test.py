import numpy as np
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv.imshow('live video',frame)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('grayscale',gray)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array((0,32,32))
    upper = np.array((255,255,255))
    mask = cv.inRange(hsv, lower, upper)
    cv.imshow('threshold',mask)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
