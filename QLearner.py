

import numpy as np
import random 

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
    self.s = 0
    self.a = 0

    action_list = range(self.num_actions)
    self.num_states = num_states
    self.alpha = alpha
    self.gamma = gamma
    self.rar = rar
    self.radr = radr
    self.dyna = dyna

        self.Q = [[0.0 for x in action_list] for x in xrange(self.num_states)]
        self.R = [[0.0 for x in action_list] for x in xrange(self.num_states)]

        self.Tc = [[[0.00000001 for k in xrange(self.num_states)] for j in xrange(self.num_actions)] for i in xrange(self.num_states)]
        self.T = [[[(1.0 / self.num_states) for k in xrange(self.num_states)] for j in xrange(self.num_actions)] for i in xrange(self.num_states)]


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        action = random.randint(0, self.num_actions-1)
        self.a = action
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):

        old_state = self.s
        old_action = self.a
        state = s_prime
        num_actions = self.num_actions
        alpha = self.alpha
        gamma = self.gamma
        reward = r

        def best_action(q, state, default=None):
          '''Return the action with highest q value for state. 
            ties are broken at random unless default is specified'''
          actions = q[state] 
          best_q_value = max(actions) 
          indices = [i for i, x in enumerate(actions) if x == best_q_value]
          if default:
            return default
          else:
            action = random.choice(indices)
            return action

        
        prand = np.random.random()
        if prand < self.rar:
            my_action = random.randint(0,num_actions-1)
        else:
            my_action = best_action(self.Q, state)
        oldv = self.Q[old_state][old_action]
        newv = self.Q[state][my_action]
        self.Q[old_state][old_action] = (1.0 - alpha) * oldv + alpha * (reward + gamma * newv)
        action = my_action




        self.Tc[old_state][old_action][state] = self.Tc[old_state][old_action][state] + 1
        self.R[old_state][old_action] = (1.0 - alpha) * self.R[old_state][old_action] + alpha * (reward)

        for h in range(0, self.num_states):            
            self.T[old_state][action][h] = self.Tc[old_state][action][h] / sum(self.Tc[old_state][action][:])
        for k in range(0, self.dyna):
            s = random.randint(0,self.num_states-1)
            a = random.randint(0, num_actions-1)
            randy = np.random.random()
            summy = 0.0
            t = 0
            while summy <= randy:
                summy = summy + self.T[s][a][t]
                s_primmy = t
                t = t + 1

            r = self.R[s][a]



            self.Q[s][a] = (1.0 - alpha) * self.Q[s][a] + alpha * (r + gamma * self.Q[s_primmy][best_action(self.Q,s_primmy)])

            
      
        self.s = s_prime
        self.a = my_action
        self.rar = self.rar * self.radr
        if self.verbose: print "s =", s_prime,"a =",action,"Q =",self.Q[old_state][my_action]

    
        return my_action
