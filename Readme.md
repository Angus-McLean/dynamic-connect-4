

# A1 - Dynamic Connect 4

Hello and Welcome 👋

This is the implementation of an _'AlphaBeta Convolutional Heuristic Agent'_ to play the Dynamic Connect 4 game optimally.

Jupyter Notebooks are the foundation of this project, then the important pieces were copied over to .py files in time for competition.

The report is best viewed by opening the `A1 - Report.htm` file.

Information about the assignment can be found on the [ECSE-526 website](http://cim.mcgill.ca/~jer/courses/ai/assignments/as1.html)

## Install
This project requires the following packages to be available. :
`scipy, telnetlib, numpy, hashlib, argparse`
They are likely already installed but they can be pip installed.


## Start your Agent

`python ./main.py --game_id="mytestgame" -c 'white' --state_file=./state_q1b.txt --host=localhost --port=12345`


__Alternative : Running Agent with Jupyter Notebook__
In order to start your agent please run "A1 - AI-Agent - AlphaBeta.ipynb". It will automatically connect to the server configured and begin playing the game.

As mentioned this logic will be extracted into .py files in time for competition so that the agent can easily be run from command line (above).


## Project Organization


File | Contents
--- | ---
`A1 - Dynamic Connect 4.ipynb` | Step-by-step Walkthrough of Implementation of Algorithms.
`A1 - Report.ipynb` | Long-form answers, graphs and codes associated with the report.
`A1 - AI-Agent - AlphaBeta.ipynb` | Small notebook for quickly configuring an agent to connect and compete against server.
__Python Files__ | (roughly in order of dependencies)
main.py | Parses input arguments
gameAgent.py | Connects to server and wraps algorithms
heuristic.py | Implementation of heuristic and search
dynamicConnect4.py | Definition of game and state
