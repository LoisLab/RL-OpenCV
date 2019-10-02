import cv2 as cv
import numpy as np
import math

'''
Observer that uses webcam to observer and report on playing field.
'''

class Observer:
    PINK = {'name':'pink','hsv':(153,155,198)}
    ORANGE = {'name':'orange','hsv':(16,147,214)}
    YELLOW = {'name':'yellow','hsv':(50,77,234)}

    def __init__(self,sat_limits=(50,200),val_limits=(128,255),detection_width=5):
        self.cap = cv.VideoCapture(0)
        self.sl = sat_limits
        self.vl = val_limits
        self.dw = detection_width
        self.update()

    def update(self):
        self.frame = self.get_frame()

    def show(self):
        cv.imshow('frame',self.frame)

    def get_frame(self):
        status, frame = self.cap.read()
        if status:
            return frame
        else:
            raise Exception('failed to read video camera')

    def get_mask(self,hsv_color):
        hsv_frame = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
        hsv_vals = hsv_color['hsv']
        lower = np.array((min(max(hsv_vals[0]-self.dw,0),255),self.sl[0],self.vl[0]))
        upper = np.array((min(max(hsv_vals[0]+self.dw,0),255),self.sl[1],self.vl[1]))
        mask = cv.inRange(hsv_frame, lower, upper)
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)
        return mask

    def get_xy_theta(self,color0,color1):
        try:
            c0,c1 = self.get_center(color0),self.get_center(color1)
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

    def get_center(self, hsv_color):
        mask = self.get_mask(hsv_color)
        contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if (len(contours)>0):
            largest = max(contours, key=cv.contourArea)
            ((x, y), radius) = cv.minEnclosingCircle(largest)
            M = cv.moments(largest)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            return center
        else:
            return None

    def test(self):
        while(True):
            self.update()
            self.show()
            for c in (Observer.PINK,Observer.ORANGE,Observer.YELLOW):
                cv.imshow(c['name'],self.get_mask(c))
            try:
                centers = {c['name']:self.get_center(c) for c in (Observer.PINK,Observer.ORANGE,Observer.YELLOW)}
                print(self.get_xy_theta(Observer.PINK,Observer.YELLOW))
            except Exception as e:
                print(e)
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        cv.destroyAllWindows()