# imports and constants

import numpy as np
import time
import re

PLAYER_IDS = {
    'color':['white','black'],
    'symbol':['O','X'],
    'num':[1,-1]
}

DIR = {
    'N':(-1,0),
    'S':(1,0),
    'E':(0,1),
    'W':(0,-1)
}

def strToState(strState):
    arrState = re.sub('^ *\n|\n *$','', strState).replace('\n',',').replace(' ','').split(',')
    arrState = np.array(arrState).reshape((7,7))
    
    a = np.where(arrState=='X', -1, arrState)
    a = np.where(a=='O', 1, a)
    matState = np.where(a=='', 0, a).astype(int)
    
    return np.matrix(matState)

def stateToStr(state):
    return ' '+re.sub('\[|\]','', re.sub(' *(-?\d)', '\g<1>,',str(state.astype(int))).replace(',]',']')).replace('-1','X').replace('1','O').replace('0',' ')

def generateMovesForPiece(state, coords):
    intPiece = state[coords]
    matAction = np.zeros((7,7))
    matAction[coords] = -1*intPiece
    actions = []
    
    
    if coords[0]+1<7:
        a1 = matAction.copy()
        a1[coords[0]+1, coords[1]] = intPiece
        actions.append(a1)
    if coords[0]-1>=0:
        a2 = matAction.copy()
        a2[coords[0]-1, coords[1]] = intPiece
        actions.append(a2)
    if coords[1]+1<7:
        a3 = matAction.copy()
        a3[coords[0], coords[1]+1] = intPiece
        actions.append(a3)
    if coords[1]-1>=0:
        a4 = matAction.copy()
        a4[coords[0], coords[1]-1] = intPiece
        actions.append(a4)
    
    return np.array(actions)

def generateMovesForPlayer(player, state):
    piecesCoords = list(zip(*np.where(state==player)))
    moves = np.concatenate(list(map(lambda c:generateMovesForPiece(state,c), piecesCoords)))
    return moves
#     return validateMoves(state, moves)

def isValidState(state):
    if state.sum() != 0 : return False
    if np.count_nonzero(state) != 12 : return False
    return True

def validateMoves(state, moves):
    nextStates = np.add(moves, np.asarray(state))
    counts = np.sum(np.count_nonzero(nextStates,axis=1), axis=1)
    m_counts = counts==12
    return moves[m_counts]


def generateSuccessorsForPlayer(player, state):
    moves = generateMovesForPlayer(player, state)
    nextStates = np.add(moves, np.asarray(state))
    counts = np.sum(np.count_nonzero(nextStates,axis=1), axis=1)
    m_counts = counts==12
    return nextStates[m_counts]


def strToMove(moveStr, player):
    moveList = tuple(moveStr[:3])
    moveArr = np.zeros((7,7))
    moveArr[int(moveList[1])-1, int(moveList[0])-1] = -1*player
    newPos = np.add(np.array(moveList[1],moveList[0]).astype(int), np.array(DIR[moveList[2]]))
    moveArr[newPos[0]-1,newPos[1]-1] = player
    return moveArr


def moveToStr(moveArr, player):
    coords = np.array(np.where(moveArr==player)).reshape(-1)
    oldCoords = np.array(np.where(moveArr==-1*player)).reshape(-1)
    movementTup = coords - oldCoords
    direction = list(DIR.keys())[list(DIR.values()).index(tuple(movementTup))]
    return '{}{}{}'.format(oldCoords[0]+1, oldCoords[1]+1, direction)