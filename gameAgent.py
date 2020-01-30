# game-agent.py
import telnetlib
import time
import re


import dynamicConnect4
import searchAlgo
import heuristic

print('Running.. game-agent.py')


SERVER_CONFIG = {
    'host' : 'localhost',
    'port' : 12345,
    'colour' : 'white',
    'game_id' : 'mytestgame',
    'state_file' : '/Users/amclean/Documents/School/ECSE 526/workspace/Assignment 1/state_q1a.txt'
}

def connectToServer(serverObj) :
    host = serverObj['host']
    port = serverObj['port']
    colour = serverObj['colour']
    game_id = serverObj['game_id']

    tn = telnetlib.Telnet(host, port)
    tn.write(bytes('{} {}\n'.format(game_id, colour), 'ascii'))
    print('waiting for game :', game_id)
    tn.read_until(bytes(game_id, 'ascii'))
    return tn

def readRemote(tnServer):
    resp = tnServer.read_until(bytes('\n', 'ascii')).decode('ascii')
    print('Reading : ', resp)
    return resp

def getRemoteMove(tnServer, state, player):
    remoteStr = readRemote(tnServer)
    if not re.match('^[1-7]{2}[NSWE]', remoteStr) : 
        print('Cannot parse to move :', remoteStr);
        return None
    
    # validate opponent is moving correct piece
    if state[int(remoteStr[0])-1, int(remoteStr[1])-1] != player:
        print('Attempting to move wrong piece :', remoteStr);
        return None

    newState = state + dynamicConnect4.strToMove(remoteStr, player)
    if not dynamicConnect4.isValidState(newState) :
        print('Invalid State from Server\n', remoteStr)
        return None
    return newState


def getAiMove(state, player, time_limit, tnServer):
    (bestScore, nextState) = searchAlgo.executeTurn(state, player, 5)
    moveArr = nextState-state
    moveStr = dynamicConnect4.moveToStr(moveArr, player)
    # print('before - send')
    tnServer.write(bytes(moveStr + '\n', 'ascii'))
    # tnServer.write(moveStr + '\n')
    # print('after - send')
    print('Wrote', moveStr, '\n')
    return nextState


def game_ai_vs_remote(serverObj=SERVER_CONFIG):

    stateFile=serverObj['state_file']
    with open(stateFile, 'r') as file:
        stateStr = file.read()
    state = dynamicConnect4.strToState(stateStr)

    tnServer = connectToServer(serverObj)
    
    time_limit = float(10000)
    moveNum = 1
    player = serverObj['colour']
    remote_turn = player == 'black'

    resp = tnServer.read_until(bytes('\n', 'ascii')).decode('ascii')
    print('ServerTurn - Reading : ', resp)
    curPlayer = dynamicConnect4.PLAYER_IDS['num'][dynamicConnect4.PLAYER_IDS['color'].index('white')]
    
    print('\n\n------ Start Game! -----')
    print('----- Move : ', moveNum-1,' Player : ',curPlayer,' LocalTurn :', not(remote_turn),' -------')
    print(dynamicConnect4.stateToStr(state))

    while True :
        start_time = time.time()
        
        if remote_turn:
            nextState = getRemoteMove(tnServer, state, curPlayer)
            if nextState is None : continue
            state=nextState
        else:
            # print('AI moving... - ',state)
            state=getAiMove(state, curPlayer, time_limit, tnServer)
            # print('AI Moved - ',state)

        print('\n\n------ Game State -----')
        print('----- Move : ', moveNum,' Player : ',curPlayer,' LocalTurn :', not(remote_turn),' -------')
        print(dynamicConnect4.stateToStr(state))
            
        if heuristic.scoreMaxConnected(curPlayer, state) == 4:
            print('======= Winner !! == Player :',curPlayer)
            print(dynamicConnect4.stateToStr(state))
            return        

        curPlayer = -1*curPlayer
        remote_turn = not remote_turn
        moveNum += 1

