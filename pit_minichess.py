import Arena
from MCTS import MCTS
from minichess.MinichessGame import MinichessGame
from minichess.MinichessMinimax import *
from minichess.NNetPlayer import *
from minichess.keras.NNet import NNetWrapper as NNet
import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = MinichessGame(5, 5)

# minimax player
minimax_p1 = MinimaxPlayer(g, 1).select_move

# nnet players
n1 = NNet(g)
n1.load_checkpoint('./temp/', 'temp.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
mcts1 = MCTS(g, n1, args1)


def n1p(x):
    return np.argmax(mcts1.getActionProb(x, temp=0))


arena = Arena.Arena(n1p, minimax_p1, g, display=g.display)
print(arena.playGames(10, verbose=True))
