import numpy as np
import argparse
from goalseek import *

ap = argparse.ArgumentParser()
ap.add_argument('-ip')
args = vars(ap.parse_args())

env = GoalSeek(args['ip'])

q = np.zeros((8,8))

obs = env.reset()
done = False

