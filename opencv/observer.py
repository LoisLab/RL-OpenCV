import cv2 as cv
import numpy as np
import math
import time

'''
Observer that uses webcam to observer and report on playing field.
'''

PINK = {'name':'pink','hsv':(153,155,198)}
ORANGE = {'name':'orange','hsv':(16,147,214)}
YELLOW = {'name':'yellow','hsv':(50,77,234)}

class Observer:

    def __init__(self,sat_limits=(50,200),val_limits=(128,255),detection_width=8,fore=PINK,aft=YELLOW, target=ORANGE):
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_BUFFERSIZE,1) # set buffer size to 1
        self.sl = sat_limits
        self.vl = val_limits
        self.dw = detection_width
        self.fore = fore
        self.aft = aft
        self.target = target
        self.frame = None
        self.warmup_capture()

    def warmup_capture(self):
        for n in range(10):
            self.cap.read()

    def update(self):
        self.frame = self.get_frame()

    def show(self):
        cv.imshow('frame',self.frame)

    def get_observation(self):
        xyt_bot = self.get_xy_theta(self.fore, self.aft)
        xyt_tgt = self.get_xy_theta(self.target, self.fore)
        distance = self.get_distance(self.fore, self.target)
        rel_bearing = xyt_bot[2]-xyt_tgt[2]
        rel_bearing += 360 if rel_bearing<-180 else 0
        return np.array(xyt_bot+xyt_tgt+(distance,)+(rel_bearing,))

    def print_obs(self,obs):
        print('x,y,t bot', obs[0:3])
        print('x,y,t tgt', obs[3:6])
        print('distance ', obs[6])
        print('bearing  ', obs[7])

    def get_frame(self):
        self.cap.read() # clear the buffer (contains 1 frame)
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
                theta = math.pi/2 if dy>0 else 3*math.pi/2
            elif dy==0:
                theta = 0 if dx>0 else math.pi
            else:
                m = abs(dy/dx)
                theta = math.atan(m)            # 1st quadrant (assumed)
                if dx<0:                        # 2nd or 3rd quadrant...
                    if dy<0:
                        theta = math.pi+theta   # ...3rd quadrant
                    else:
                        theta = math.pi-theta   # ...2nd quadrant
                elif dy<0:
                    theta = 2*math.pi-theta     # 4th quadrant
            alpha = theta*360.0/(math.pi*2)
            alpha += 360 if alpha < 0 else 0
            return ((c0[0]+c1[0])/2,(c0[1]+c1[1])/2,alpha)

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

    def get_distance(self,color0,color1):
        c0 = self.get_center(color0)
        if c0 is None:
            raise Exception('cannot detect color: ' + color0['name'])
        c1 = self.get_center(color1)
        if c1 is None:
            raise Exception('cannot detect color: ' + color1['name'])
        dx = float(c0[0]-c1[0])
        dy = float(c0[1]-c1[1])
        return (dx**2+dy**2)**0.5

    def test(self,delay=0):
        while(True):
            time.sleep(delay)
            self.update()
            self.show()
            for c in (PINK,ORANGE,YELLOW):
                cv.imshow(c['name'],self.get_mask(c))
            try:
                heading = self.get_xy_theta(self.fore,self.aft)[2]
                abs_bearing = self.get_xy_theta(self.target,self.fore)[2]
                rel_bearing = heading - abs_bearing
                rel_bearing += 360 if rel_bearing<-180 else 0
                print(self.get_center(ORANGE),\
                      self.get_center(YELLOW),\
                      self.get_center(PINK),\
                      'distance=',\
                      '{:+.2f}'.format(self.get_distance(PINK,ORANGE)),\
                      'heading=',\
                      '{:+.2f}'.format(heading),\
                      'abs bearing',\
                      '{:+.2f}'.format(abs_bearing),\
                      'rel bearing',\
                      '{:+.2f}'.format(rel_bearing))
                print(self.get_observation())
            except Exception as e:
                print(e)
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        cv.destroyAllWindows()

    def __str__(self):
        self.update()
        obs = self.get_observation()
        print('xyt bot', obs[0:2])
        print('xyt tgt', obs[3:6])
        print
