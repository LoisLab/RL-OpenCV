import HttpBot

'''
Goal seeking reinforcement-learning environment for minibot
'''

class GoalSeek:
    action_space = [x for x in range(8)]

    def __init__(self,ip):
        bot = HttpBot(ip)
        observer = Camera()

    def reset(self):
        pass

    def step(self,action):
        bot.step(action)
