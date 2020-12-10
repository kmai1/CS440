import numpy as np
import utils
import random


class Agent:

    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma
        self.s = None
        self.a = None
        self.points = 0
        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        # reset in init maybe
        self.reset()

    def train(self):
        self._train = True

    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)
        utils.save(model_path.replace('.npy', '_N.npy'), self.N)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        Each state in the MDP is a tuple (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right).

        '''
        # reward case, if u die u reset
        # if (dead):
        #     reset(self)

        # #movements
        # up = 0
        # down = 1
        # left = 2
        # right = 3
        #u is Q(s,a) and n is N(s,a)
        def f(u, n):
            if n < self.Ne:
                return 1
            else:
                return u
        def rewardFunction(points, myPoints, dead):
            if dead:
                return -1
            if points > myPoints:
                return 1
            return -0.1

        snake_head = [state[0], state[1]]
        snake_body = state[2] #might need to deep copy
        food = [state[3], state[4]]
        adjoining_wall_x = 0
        adjoining_wall_y = 0

        if snake_head[0] == 40:
            adjoining_wall_x = 1 #left
        if snake_head[0] == 480:
            adjoining_wall_x = 2 #right
        if snake_head[1] == 40:
            adjoining_wall_y = 1 #top
        if snake_head[1] == 480:
            adjoining_wall_y = 2 #bottom

        adjoining_wall = [adjoining_wall_x, adjoining_wall_y]

        food_x_loc = 0
        food_y_loc = 0

        if snake_head[0] < food[0]:
            food_x_loc = 2 #right
        if snake_head[0] > food[0]:
            food_x_loc = 1 #left
        if snake_head[1] > food[1]:
            food_y_loc = 1 #bottom
        if snake_head[1] < food[1]:
            food_y_loc = 2 #top

        food_loc = [food_x_loc, food_y_loc]

        adjoining_body_left, adjoining_body_right, adjoining_body_top, adjoining_body_bottom = 0, 0, 0, 0
        if (snake_head[0] + 40, snake_head[1]) in snake_body:
            adjoining_body_right = 1
        if (snake_head[0] - 40, snake_head[1]) in snake_body:
            adjoining_body_left = 1
        if (snake_head[0], snake_head[1] + 40) in snake_body:
            adjoining_body_bottom = 1
        if (snake_head[0], snake_head[1] - 40) in snake_body:
            adjoining_body_top = 1

        MDP_state = (adjoining_wall[0], adjoining_wall[1], food_loc[0], food_loc[1], adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right)

        # training piazza 1443
        # alpha is always C/(C+N) or maybe C/(C+N(s,a) + 1)
        #self.s wil be prev state
        s_prime = MDP_state #curr state
        reward = rewardFunction(points, self.points, dead)
        if self._train:
            # reward = rewardFunction(points, self.points, dead)
            if self.s != None and self.a != None: #once there is a prev state and action, then do this qtable stuff
                # update q table
                # reward = rewardFunction(points, self.points, dead)
                alpha = self.C / (self.C + self.N[self.s + (self.a,)]) #self.N ???
                Q = self.Q #this is a q-table
                #formula on mp page under q-learning agent
                Q[self.s + (self.a,)] = Q[self.s + (self.a,)] + alpha * (reward + self.gamma * np.max(Q[s_prime]) - Q[self.s + (self.a,)])

            #exploration policy is next tiebreak is 3 2 1 0??? right left down up for this, make some f function

            Ns = self.N[s_prime]
            if dead:
                self.reset()
                return
            temp = []
            moves = [3, 2, 1, 0]
            for movements in moves:
                u = self.Q[s_prime + (movements,)]
                n = self.N[s_prime + (movements,)]
                temp.append(f(u, n))
                # print(f(u,n))
            a = np.argmax(temp) #index of max
            # print(a)
            action = moves[a]
            #die
            Ns[action] += 1 #update times move occured
            self.s = s_prime #update prev pos
            self.a = action #updates prev action
            self.points = points #updates prev points
            # if dead:
            #     self.reset()
            #     return
            return action
        if not self._train:
            temp = []
            moves = [3, 2, 1, 0]
            for movements in moves:
                temp.append(self.Q[s_prime + (movements,)])
            a = np.argmax(temp)
            action = moves[a]
            return action
        if dead:
            self.reset()
            return
