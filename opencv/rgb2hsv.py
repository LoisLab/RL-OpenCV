import cv2 as cv
import argparse
import numpy as np

'''
Converts RGB to HSV (using the HSV ranges native to OpenCV)
'''

ap = argparse.ArgumentParser()
ap.add_argument('-r')
ap.add_argument('-g')
ap.add_argument('-b')
args = vars(ap.parse_args())

red = int(args['r'])
blue = int(args['b'])
green = int(args['g'])

bgr = np.uint8([[[blue,green,red]]])
print('bgr',bgr)
hsv = cv.cvtColor(bgr,cv.COLOR_BGR2HSV)
print('hsv',hsv)
