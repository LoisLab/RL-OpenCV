import cv2 as cv
import numpy as np
import math

'''
Proof of concept for tracking x,y,theta for a mini-robot using
colored post-its and a webcam.
'''

HSV_POSTIT_PINK = {'name':'pink','hsv':(153,155,198)}
HSV_POSTIT_ORANGE = {'name':'orange','hsv':(16,147,214)}
HSV_POSTIT_YELLOW = {'name':'yellow','hsv':(50,77,234)}

def get_xy_theta(hsv,color0,color1):
	try:
		c0,c1 = get_center(hsv,color0),get_center(hsv,color1)
		dy,dx = c1[1]-c0[1], c1[0]-c0[0]
		if dx==0:
			m = math.inf * (-1 if dy<0 else 1)
			theta = math.atan(m)
		else:
			m = abs(dy/dx)
			theta = math.atan(m)
		# arctan has a limited domain...
		if dx<0 and dy>=0:
			theta = math.pi-theta
		elif dx<0 and dy<0:
			theta = math.pi+theta
		elif dx>=0 and dy<0:
			theta = math.pi*2-theta
		alpha = theta*360.0/(math.pi*2)
		return (c0[0]+dx/2,c0[1]+dy/2,alpha)
	except Exception as e:
		print(e)
		return None

def get_center(hsv_frame, hsv, width=5, s=(50,200), v=(128,255), render=False):
	hsv_vals = hsv['hsv']
	lower = np.array((min(max(hsv_vals[0]-width,0),255),s[0],v[0]))
	upper = np.array((min(max(hsv_vals[0]+width,0),255),s[1],v[1]))
	mask = cv.inRange(hsv_frame, lower, upper)
	mask = cv.erode(mask, None, iterations=2)
	mask = cv.dilate(mask, None, iterations=2)
	if render:
		cv.imshow(hsv['name'],mask)
	contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	if (len(contours)>0):
		largest = max(contours, key=cv.contourArea)
		((x, y), radius) = cv.minEnclosingCircle(largest)
		M = cv.moments(largest)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		return center
	else:
		return None

cap = cv.VideoCapture(0)
while(True):
	# Take each frame
	_, frame = cap.read()
	# Convert BGR to HSV
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	try:
		centers = {c['name']:get_center(hsv, c, render=True) for c in (HSV_POSTIT_PINK,HSV_POSTIT_ORANGE,HSV_POSTIT_YELLOW)}
		print(get_xy_theta(hsv,HSV_POSTIT_PINK,HSV_POSTIT_YELLOW))
	except Exception as e:
		print(e)

	cv.imshow('frame',frame)

	k = cv.waitKey(5) & 0xFF
	if k == 27:
		break
cv.destroyAllWindows()
