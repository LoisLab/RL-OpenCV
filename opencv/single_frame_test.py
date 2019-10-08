import numpy as np
import cv2 as cv
import numpy as np

def snap(camera):
    ret, frame = camera.read()  # clear frame buffer (contains 1 frame)
    ret, frame = camera.read()
    cv.imshow('single frame',frame)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('grayscale',gray)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower = np.array((0,32,32))
    upper = np.array((255,255,255))
    mask = cv.inRange(hsv, lower, upper)
    cv.imshow('threshold',mask)

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_BUFFERSIZE,1) # set buffer size to 1
snap(cap)

done = False
while not done:
    while True:
        k = cv.waitKey(5) & 0xFF
        if k == 32:
            snap(cap)
        done = k==27

# release the capture
cap.release()
cv.destroyAllWindows()
