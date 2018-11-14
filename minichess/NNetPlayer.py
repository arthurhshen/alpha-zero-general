from minichess.MinichessGame import display
from minichess.MinichessLogic import Board
# from minichess.MiniChessUtil import *
# from minichess.MiniChessConstants import *
from minichess.keras.NNet import NNetWrapper as NNet
from MCTS import MCTS
from utils import *

class NNetPlayer():
    def __init__(self, game, ckpt_path, ckpt_file, args):
        self.nnet = NNet(game)
        self.args = dotdict(args)
        self.nnet.load_checkpoint(ckpt_path, ckpt_file)
        self.mcts = MCTS(game, self.nnet, self.args)

    def play(self, board):
        tmp = self.args["temp"] if "temp" in self.args else 0
        move = np.argmax(self.mcts.getActionProb(board, temp=tmp))
        return move
