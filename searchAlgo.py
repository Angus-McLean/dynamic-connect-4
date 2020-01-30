## search-algo.py

import dynamicConnect4
import heuristic

from hashlib import sha1
import numpy as np
import time
import re

DB_TRANSP = {}
DB_STATE = {}
def put(state):
    strHash = sha1(state.tobytes()).hexdigest()
    DB_STATE[strHash] = state
    return strHash

def get(strHash):
    return DB_STATE[strHash]


def executeTurn(state, player, depth):
    arrSuccessors = dynamicConnect4.generateSuccessorsForPlayer(player, state)
    actionValues = [heuristic.scoreMaxConnected(player, st) for st in arrSuccessors]
    if max(actionValues) >= 4:
        return (max(actionValues), arrSuccessors[actionValues.index(max(actionValues))])
    return alphaBetaHeuristic(put(state), player, depth)


def alphaBetaHeuristic(stateStr, player, depth, alpha=-np.inf, beta=np.inf, heuristic=heuristic.fuzzyHeuristic):
    if hasattr(alphaBetaHeuristic, 'count'): alphaBetaHeuristic.count = alphaBetaHeuristic.count+1
    if (depth, stateStr) in DB_TRANSP: return DB_TRANSP[(depth, stateStr)]
    state = get(stateStr)
    score = heuristic(player*-1, state)*player*-1
    if depth==0 or abs(score)>=1:
        return (score, state)
    
    actionValues = []
    arrSuccessors = dynamicConnect4.generateSuccessorsForPlayer(player, state)

    for st in arrSuccessors:
        v, _ = alphaBetaHeuristic(put(st), player*-1, depth-1, alpha, beta)
        
        actionValues.append(v)
        if player>0:
            alpha = max(alpha, v)
        else :
            beta = min(beta, v)
        if beta <= alpha:
            break
    
    bestScore = max(actionValues) if (player > 0) else min(actionValues)
    DB_TRANSP[(depth, stateStr)] = (bestScore, arrSuccessors[actionValues.index(bestScore)])
    return DB_TRANSP[(depth, stateStr)]

print('done!')