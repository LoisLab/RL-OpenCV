import numpy as np
from opencv.observer import *
from minibot.http_bot import *

'''
Goal seeking reinforcement-learning environment for minibot
'''

class GoalSeek:
    actions = [x for x in range(8)]

    def __init__(self,ip,delay=0.4):
        self.bot = HttpBot(ip)
        self.observer = Observer()
        self.delay = delay

    def reset(self):
        self.observer.update()
        return self.observer.get_observation()

    def step(self,action):
        try:
            self.observer.update()
            d0 = self.observer.get_distance(self.observer.fore,self.observer.target)
            self.bot.step(action)
            time.sleep(self.delay)
            self.observer.update()
            d1 = self.observer.get_distance(self.observer.fore,self.observer.target)
            done = d1<70
        except Exception as e:
            print(e)
            done = True
        return self.observer.get_observation(), d0-d1, done

    def sample(self):
        return np.random.choice(GoalSeek.actions)
