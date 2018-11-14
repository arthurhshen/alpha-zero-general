from Coach import Coach
# from othello.OthelloGame import OthelloGame as Game
from minichess.MinichessGame import MinichessGame as Game
from minichess.MinichessLogic import Board

from othello.pytorch.NNet import NNetWrapper as nn
from utils import *
import sys 

args = dotdict({
    'numIters': 1000,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__ == "__main__":
    g = Game(5, 5)
    nnet = nn(g)
    b = Board()

    if len(sys.argv) > 1:
        if sys.argv[1] in ('--console', '-c'):
            from gui import display
            display(b)
            exit(0)
        elif sys.argv[1] in ('--help', '-h'):
            print ('''Usage: game.py [OPTION]\n\n\tPlay a game of chess\n\n\tOptions:\n\t -c, --console\tplay in console mode\n\n''')
            exit(0)

    try:
        from gui import display
    except ImportError:
        from gui import display
    finally:
        display(b)
'''
    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
'''