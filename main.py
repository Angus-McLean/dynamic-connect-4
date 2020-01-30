## main.py

from argparse import ArgumentParser
import gameAgent

def run(args):
    gameAgent.game_ai_vs_remote(serverObj=args)



if __name__ == '__main__':

    parser = ArgumentParser(description='Description of your program')

    parser.add_argument('--host', default='localhost')
    parser.add_argument('-p', '--port', default=12345, type=int)
    parser.add_argument('-c', '--colour', default='white')
    parser.add_argument('-g', '--game_id', default='mytestgame')
    parser.add_argument('-s', '--state_file', default='/Users/amclean/Documents/School/ECSE 526/workspace/Assignment 1/state_q1a.txt')
    
    args = vars(parser.parse_args())

    print('Starting Agent -- Let the games begin!!')
    run(args)
    