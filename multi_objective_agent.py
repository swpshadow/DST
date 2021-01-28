
# to call: python3 multi_objective_agent.py [number of episodes] [time objective weight] [treasure objective weight]
# sample function call: python3 multi_objective_agent.py 50000 0.7 0.3
#

import os
import sys
from collections import deque
from collections import defaultdict
from statistics import mean
from openpyxl import load_workbook

import numpy as np
import matplotlib.pyplot as plt

import dst_environment
from dst_environment import *

class agent:
    def __init__(self, env):
        self.env = env
        self.explore_rate = 1
        self.alpha = .2
        self.gamma = 0.9
        self.q = {k: 0 for k in [ (x, y, z) for x in range(0,11) for y in range(0,10) for z in range(0,4)]}

    def nextAction(self, state):
        if random.random() < self.explore_rate:
            return random.sample(self.env.get_available_actions(state[0]), k=1)[0]
        actions = self.env.get_available_actions(state[0])
        maxx = max(range(len(actions)), key=lambda x: [self.q[state[0], state[1], a] for a in actions][x])
        return actions[maxx]

    def update(self, state, action, reward, new_state, done):
        if done:
            self.q[state[0], state[1], action] += self.alpha * (reward - self.q[state[0], state[1], action])
        else:
            maxq = max([self.q[new_state[0], new_state[1], a] for a in self.env.get_available_actions(new_state[0])])
            self.q[state[0], state[1], action] += self.alpha * ( reward + self.gamma * maxq - self.q[state[0], state[1], action])
    def print_q(self):
        print(self.q)

total_rounds = 1000
beta = 1
alpha = 1
if len(sys.argv) > 1:
    total_rounds = int(sys.argv[1])
if len(sys.argv) > 2:
    alpha = float(sys.argv[2])

if len(sys.argv) > 3:
    beta = float(sys.argv[3])

env = dst_environment(beta, alpha)
a = agent(env)
state = [0,0]
reward = [0,0]
count = 0
final_reward = [0,0]


while True:
    action = a.nextAction(state)
    new_state = env.take_action(action)
    r = env.get_reward()
    if r[1] < 1:
        a.update(state, action, alpha * r[0] + beta * r[1], new_state, False)
        reward[0] += r[0]
        state = new_state
    else:
        count +=1
        reward[0] += r[0]
        reward[1] += r[1]
        sys.stdout.write("\rrounds complete: {} explore rate: {}".format(count, a.explore_rate))
        sys.stdout.flush()
        a.update(state, action, alpha * r[0] + beta * r[1], new_state, True)
        env.reset_round()
        state = [0,0]
        if count < total_rounds - 10:
            a.explore_rate = max( (1 - (count / total_rounds) ) **2, 0.05 )
            a.alpha =  max( (1 - (count / total_rounds) ) **2, 0.01)
        else:
            a.explore_rate = 0
            final_reward[0] = reward[0]
            final_reward[1] = reward[1]
        if count >= total_rounds:
            a.print_q()
            break
        reward = [0,0]

print("\n")

print("final reward: ", final_reward[0], final_reward[1])