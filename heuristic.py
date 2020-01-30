## search_heuristic.py
import numpy as np

# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.filters.convolve.html
from scipy import ndimage
# https://stackoverflow.com/questions/41418717/checking-if-adjacent-values-are-in-a-numpy-matrix
from scipy.ndimage import label

filtDiag4 = np.diag((1,1,1,1))
filtDiagx4 = np.flip(filtDiag4, axis=0)
filtFlat4 = [[1,1,1,1]]
filtVert4 = [[1], [1], [1], [1]]

fuzzyFiltDiag4 = np.array([
    [1,1,0,0,0,0],
    [1,2,1,0,0,0],
    [0,1,2,1,0,0],
    [0,0,1,2,1,0],
    [0,0,0,1,2,1],
    [0,0,0,0,1,1]
])
fuzzyFiltDiagx4 = np.flip(fuzzyFiltDiag4, axis=0)
fuzzyFiltFlat4 = np.array([[0,1,1,1,1,0], [1,2,2,2,2,1], [0,1,1,1,1,0]])
fuzzyFiltVert4 = fuzzyFiltFlat4.T


def scoreMaxConnected(player, state):
    pieces = (state==player).astype(int)
    flatCount = ndimage.convolve(pieces, filtFlat4, mode='constant', cval=0.0).max()
    vertCount = ndimage.convolve(pieces, filtVert4, mode='constant', cval=0.0).max()
    diagCount = ndimage.convolve(pieces, filtDiag4, mode='constant', cval=0.0).max()
    diagxCount = ndimage.convolve(pieces, filtDiagx4, mode='constant', cval=0.0).max()
    return np.max((flatCount, vertCount, diagCount, diagxCount))


def scoreMaxConnectedFuzzy(player, state):

    flatCount = ndimage.convolve(state, fuzzyFiltFlat4, mode='constant', cval=0.0)
    vertCount = ndimage.convolve(state, fuzzyFiltVert4, mode='constant', cval=0.0)
    diagCount = ndimage.convolve(state, fuzzyFiltDiag4, mode='constant', cval=0.0)
    diagxCount = ndimage.convolve(state, fuzzyFiltDiagx4, mode='constant', cval=0.0)
    fuzzyScores = np.array([flatCount, vertCount, diagCount, diagxCount])
    return np.max(fuzzyScores) if player == 1 else np.min(fuzzyScores)
#     return fuzzyScores[np.argmax(np.abs(fuzzyScores))]

def fuzzyHeuristic(player, state):
    return (scoreMaxConnected(player, state) + scoreMaxConnectedFuzzy(player, state)/8)/4

