agentMin = float("inf")
agentMax = -float("inf")
        
def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0
    self.evaluationFunction = util.lookup(evalFn, gloabls())
    self.depth = int(depth)
    self.agentMin = float("inf")
    self.agentMax = -float("inf")

def AlphaBetaHelper(self, state, agent, ply):
        if (state.isWin() | state.isLose()):
            return self.evaluationFunction(state)
     
        agentMoves = state.getLegalActions(agent)
        agentNum = state.getNumAgents()

        if ((agent == agentNum - 1) & (ply == self.depth)):
            terminalState = util.PriorityQueue()
            for agentState in [state.generateSuccessor(agent, move) for move in agentMoves]:
                terminalState.push(agentState, self.evaluationFunction(agentState))
                if (self.evaluationFunction(agentState) < agentMax):
                    break
            terminalState = terminalState.pop()
            agentMax = max(agentMax, terminalState)
            return self.evaluationFunction(terminalState)
     
        elif (agent == 0):
            pacMax = util.PriorityQueue()
            for agentState in [state.generateSuccessor(agent, move) for move in agentMoves]:
                minimax = self.MiniMaxHelper(agentState, (agent+1)%agentNum, ply)
                pacMax.push(minimax, -minimax)
                if (minimax > agentMin):
                    break
            pacMax = pacMax.pop()
            agentMin = min(agentMin, pacMax)
            return pacMax

        elif ((agent != 0)):
            lastGhost = (agent == (agentNum - 1))
            ghostMin = util.PriorityQueue()
            for agentState in [state.generateSuccessor(agent, move) for move in agentMoves]:
                minimax = self.MiniMaxHelper(agentState, (agent+1)%agentNum, ply+lastGhost)
                ghostMin.push(minimax, minimax)
                 if (minimax < agentMax):
                    break
            ghostMin = ghostMin.pop()
            agentMax = max(agentMax, ghostMin)
            return ghostMin
