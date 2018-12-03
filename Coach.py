from collections import deque
from Arena import Arena
from MCTS import MCTS
import numpy as np
from pytorch_classification.utils import Bar, AverageMeter
import time
import os
import sys
from pickle import Pickler, Unpickler
from random import shuffle
import random


class Coach():
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.game)  # the competitor network
        self.args = args
        self.mcts = MCTS(self.game, self.nnet, self.args)
        self.trainExamplesHistory = []    # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False  # can be overriden in loadTrainExamples()

    def executeEpisode(self):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.
        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.
        Returns:
            trainExamples: a list of examples of the form (canonicalBoard,pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        trainExamples = []
        board = self.game.getInitBoard()
        self.curPlayer = 1
        episodeStep = 0

        # Three fold repetition
        seen_positions = dict()

        # Fifty move count
        depth = 0

        while True:
            episodeStep += 1
            canonicalBoard = self.game.getCanonicalForm(board, self.curPlayer)

            temp = int(episodeStep < self.args.tempThreshold)

            pi = self.mcts.getActionProb(canonicalBoard, temp=temp)
            sym = self.game.getSymmetries(canonicalBoard, pi)
            for b, p in sym:
                trainExamples.append([b, self.curPlayer, p, None])
            print("\n========NEW MOVE=========")
            print("player: ", self.curPlayer)
            print("current board:")
            self.game.display(board)
            action = np.random.choice(len(pi), p=pi)
            print("action: ")
            print(self.game.index_dict[action])

            # Check to see if a pawn was moved, or if a piece was captured
            start_square, end_square = self.game.index_dict[action]

            # print("Action: ", a)
            # display(canonicalBoard)
            if abs(board[start_square[0]][start_square[1]]) == 1:
                # print(abs(canonicalBoard[start_square[0]][start_square[1]]))
                depth = 0
            elif board[end_square[0]][end_square[1]] != 0:
                # print(canonicalBoard[end_square[0]][end_square[1]])
                depth = 0
            else:
                depth = depth + 1

            if depth >= 100:
                r = 1e-8
                self.curPlayer *= -1
                return [(x[0], x[2], r * ((-1)**(x[1] != self.curPlayer))) for x in trainExamples]

            board_string = self.game.stringRepresentation(board)
            if board_string in seen_positions:
                seen_positions[board_string] += 1
                if seen_positions[board_string] >= 3:
                    r = 1e-8
                    self.curPlayer *= -1
                    return [(x[0], x[2], r * ((-1)**(x[1] != self.curPlayer))) for x in trainExamples]

            else:
                seen_positions[board_string] = 1

            try:
                board, self.curPlayer = self.game.getNextState(board, self.curPlayer, action)
            except AssertionError:
                # Redo everythign from start
                self.curPlayer *= -1
                canonicalBoard = self.game.getCanonicalForm(board, self.curPlayer)

                temp = int(episodeStep < self.args.tempThreshold)

                pi = self.mcts.getActionProb(canonicalBoard, temp=temp)
                sym = self.game.getSymmetries(canonicalBoard, pi)
                for b, p in sym:
                    trainExamples.append([b, self.curPlayer, p, None])
                print("\n========NEW MOVE=========")
                print("player: ", self.curPlayer)
                print("current board:")
                self.game.display(board)
                action = np.random.choice(len(pi), p=pi)
                print("action: ")
                print(self.game.index_dict[action])

                # Check to see if a pawn was moved, or if a piece was captured
                start_square, end_square = self.game.index_dict[action]

                # print("Action: ", a)
                # display(canonicalBoard)
                if abs(board[start_square[0]][start_square[1]]) == 1:
                    # print(abs(canonicalBoard[start_square[0]][start_square[1]]))
                    depth = 0
                elif board[end_square[0]][end_square[1]] != 0:
                    # print(canonicalBoard[end_square[0]][end_square[1]])
                    depth = 0
                else:
                    depth = depth + 1

                if depth >= 100:
                    r = 1e-8
                    # Reverse self.curPlayer if the game terminates early
                    self.curPlayer *= -1
                    return [(x[0], x[2], r * ((-1)**(x[1] != self.curPlayer))) for x in trainExamples]

                board_string = self.game.stringRepresentation(board)
                if board_string in seen_positions:
                    seen_positions[board_string] += 1
                    if seen_positions[board_string] >= 3:
                        r = 1e-8
                        self.curPlayer *= -1
                        return [(x[0], x[2], r * ((-1)**(x[1] != self.curPlayer))) for x in trainExamples]

                else:
                    seen_positions[board_string] = 1

            r = self.game.getGameEnded(board, self.curPlayer)

            if r != 0:
                self.game.display(board)
                if r == 1:
                    print ("Player -1 Wins")
                if r == -1:
                    print ("Player 1 Wins")
                else:
                    print ("Draw")
                return [(x[0], x[2], r * ((-1)**(x[1] != self.curPlayer))) for x in trainExamples]

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.args.numIters + 1):
            # bookkeeping
            print('------ITER ' + str(i) + '------')
            # examples of the iteration
            if not self.skipFirstSelfPlay or i > 1:
                iterationTrainExamples = deque([], maxlen=self.args.maxlenOfQueue)

                eps_time = AverageMeter()
                bar = Bar('Self Play', max=self.args.numEps)
                end = time.time()

                for eps in range(self.args.numEps):
                    self.mcts = MCTS(self.game, self.nnet, self.args)   # reset search tree

                    # Drop 80% of draws
                    examples = self.executeEpisode()
                    to_add = False
                    loss_rate = self.args.filter_draw_rate

                    if abs(examples[0][2]) != 1:
                        if random.random() >= loss_rate:
                            to_add = True
                    else:
                        to_add = True
                    if to_add:
                        iterationTrainExamples += examples

                    # iterationTrainExamples = self.executeEpisode()

                    # bookkeeping + plot progress
                    eps_time.update(time.time() - end)
                    end = time.time()
                    bar.suffix = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps + 1, maxeps=self.args.numEps, et=eps_time.avg,
                                                                                                               total=bar.elapsed_td, eta=bar.eta_td)
                    bar.next()
                bar.finish()

                # save the iteration examples to the history
                self.trainExamplesHistory.append(iterationTrainExamples)

            if len(self.trainExamplesHistory) > self.args.numItersForTrainExamplesHistory:
                print("len(trainExamplesHistory) =", len(self.trainExamplesHistory), " => remove the oldest trainExamples")
                self.trainExamplesHistory.pop(0)
            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)
            self.saveTrainExamples(i - 1)

            # shuffle examlpes before training
            trainExamples = []
            for e in self.trainExamplesHistory:
                trainExamples.extend(e)
            shuffle(trainExamples)

            # training new network, keeping a copy of the old one
            self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            self.pnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            pmcts = MCTS(self.game, self.pnet, self.args)

            self.nnet.train(trainExamples)
            nmcts = MCTS(self.game, self.nnet, self.args)

            print('PITTING AGAINST PREVIOUS VERSION')
            arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                          lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), self.game)
            pwins, nwins, draws = arena.playGames(self.args.arenaCompare)

            print('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
            if pwins + nwins > 0 and float(nwins) / (pwins + nwins) < self.args.updateThreshold:
                print('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            else:
                print('ACCEPTING NEW MODEL')
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename=self.getCheckpointFile(i))
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='best.pth.tar')

    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration) + ".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], self.args.load_folder_file[1])
        examplesFile = modelFile + ".examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with trainExamples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with trainExamples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True
