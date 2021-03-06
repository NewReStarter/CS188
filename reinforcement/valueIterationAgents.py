# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for iterCount in range(self.iterations):
            allStates = self.mdp.getStates()
            newValues = util.Counter()
            for state in allStates:
                allValues = list()
                possibleActions = self.mdp.getPossibleActions(state)
                if (len(possibleActions) == 0):
                    #newValues[state] = 0
                    continue
                for action in possibleActions:
                    value = self.computeQValueFromValues(state, action)
                    allValues.append(value)
                newValues[state] = max(allValues)
            self.values = newValues
            

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0
        tStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for stateAndProb in tStatesAndProbs:
            nextState = stateAndProb[0]
            prob = stateAndProb[1]
            qValue += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
        return qValue
            

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possibleActions = self.mdp.getPossibleActions(state)
        if (self.mdp.isTerminal(state) | (len(possibleActions) == 0) ):
            return None
        allActionValues = util.Counter()
        for action in possibleActions:
            allActionValues[action] = self.computeQValueFromValues(state, action)
        return allActionValues.argMax()
        
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        iterCount = 0
        stateCount = 0
        newValues = util.Counter()
        while (iterCount < self.iterations):
            allStates = self.mdp.getStates()
            state = allStates[stateCount]
            allValues = list()
            possibleActions = self.mdp.getPossibleActions(state)
            iterCount += 1
            stateCount = (stateCount + 1) % len(allStates)
            if ((len(possibleActions) == 0) | self.mdp.isTerminal(state)):
                continue
            for action in possibleActions:
                value = self.computeQValueFromValues(state, action)
                allValues.append(value)
            self.values[state] = max(allValues)
                
        
class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        diffQueue = util.PriorityQueue()
        for state in self.mdp.getStates():
            allValues = list()
            possibleActions = self.mdp.getPossibleActions(state)
            if ((len(possibleActions) == 0) | self.mdp.isTerminal(state)):
                continue
            for action in possibleActions:
                value = self.computeQValueFromValues(state, action)
                allValues.append(value)
            diff = abs(self.values[state] - max(allValues))
            diffQueue.push(state, -diff)
        for iterCount in range(self.iterations):
            if (diffQueue.isEmpty()):
                break
            state = diffQueue.pop()
            if (not self.mdp.isTerminal(state)):
                allValues = list()
                possibleActions = self.mdp.getPossibleActions(state)
                for action in possibleActions:
                    value = self.computeQValueFromValues(state, action)
                    allValues.append(value)
                self.values[state] = max(allValues)
                for predecessor in self.mdp.getStates():
                    allValues = list()
                    nextStates = list()
                    possibleActions = self.mdp.getPossibleActions(predecessor)
                    if ((len(possibleActions) == 0) | self.mdp.isTerminal(predecessor)):
                        continue
                    for action in possibleActions:
                        for tStatesAndProbs in self.mdp.getTransitionStatesAndProbs(predecessor, action):
                            nextStates.append(tStatesAndProbs[0])
                        value = self.computeQValueFromValues(predecessor, action)
                        allValues.append(value)
                    diff = abs(self.values[predecessor] - max(allValues))
                    if ((state in nextStates) & (diff > self.theta)):
                        diffQueue.push(predecessor, -diff)
            

