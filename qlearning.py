import numpy as np
import argparse
from goalseek import *

'''
simplied Q-learning for the minibot
'''

# cheater function to give simplest possible discrete state
def discrete_state(obs):
    # peek at relative bearing, shift to 60-degree centered sectors
    bearing = obs[7]
    return int(0 if (bearing+30)//60>5 else (bearing+30)//60)

ap = argparse.ArgumentParser()
ap.add_argument('-ip')
ap.add_argument('-speed')
args = vars(ap.parse_args())

env = GoalSeek(args['ip'])

if 'speed' in args:
    env.bot.set_speed(float(args['speed']))

q = (np.random.random((6,len(env.actions)))-0.5)/100.0

explore = 0.1
alpha = 0.1
gamma = 0.9

obs = env.reset()
state = discrete_state(obs)
done = False
while not done:
    if np.random.random() < explore:
        action = env.sample()
    else:
        action = np.argmax(q[state])
    obs,reward,done = env.step(action)
    new_state = discrete_state(obs)
    q[state][action] = (1-alpha)*q[state][action] + alpha*(reward+gamma*np.max(q[new_state]))
    state = new_state
    print(q)
