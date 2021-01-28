
class dst_environment:
    def __init__(self, time_penalty = .01, alpha = 1):
        self.r = 0
        self.alpha = -alpha
        self.beta = -time_penalty
        self.reward = 0
        self.loc = [0,0]
        self.terminals = self.get_terminals()
        self.states = self.get_all_states()

    def get_available_actions(self, curr_state):
        return [0, 1, 2, 3] #up, down, left, right


    def get_terminals(self):
        terminals = [ (1,0), (2,1), (3, 2), (4,3), (4,4), (4,5), (7,6), (7,7), (9, 8), (10, 9), (5, 5), (5, 6), (8,7)]
        return terminals

    def get_all_states(self):
        states = [ [-1 for _ in range(0,10)] for _ in range(0,11)] 
        states[1][0] = 1
        states[2][1] = 2
        states[3][2] = 3
        states[4][3] = 5
        states[4][4] = 8
        states[4][5] = 16
        states[7][6] = 24
        states[7][7] = 50
        states[9][8] = 74
        states[10][9] = 124
        return states


    def take_action(self, action):
        if action== 0:
            self.loc = [min(self.loc[0] + 1, 10) , self.loc[1]] 
        if action== 1:
            self.loc = [max(self.loc[0] -1, 0), self.loc[1]] 
        if action== 2:
            self.loc = [self.loc[0], max(self.loc[1] - 1, 0)] 
        if action== 3:
            self.loc = [self.loc[0], min(self.loc[1] + 1, 9) ]
        return self.loc

    def get_reward(self):
        if self.is_terminal(self.loc): 
            # print(self.states[self.loc[0]][self.loc[1]])
            return [-1, self.states[self.loc[0]][self.loc[1]]]
        else:
            return [-1, 0]

    def is_terminal(self, state):
        for i in range(len(self.terminals)):
            if state[0] == self.terminals[i][0] and state[1] == self.terminals[i][1]:
                # print(state)
                return True
        return False

    def reset_round(self):
        self.loc = [0,0]
