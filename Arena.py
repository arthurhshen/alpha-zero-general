import numpy as np
from pytorch_classification.utils import Bar, AverageMeter
import time


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """

        '''
        # Add 50 move rule and repetitions

        # counts half moves (will need to get to 100)
        moves_no_progress = 0

        # 3 fold repetition
        seen_positions = dict()
        '''

        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        while self.game.getGameEnded(board, curPlayer) == 0:
            it += 1
            if verbose:
                assert(self.display)
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.display(board)
            action = players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer))

            valids = self.game.getValidMoves(self.game.getCanonicalForm(board, curPlayer), 1)
            # print(valids)

            if valids[action] == 0:
                print(action)
                for i in range(len(valids)):
                    if valids[i] == 1:
                        print(self.game.index_dict[i])
                assert valids[action] > 0

            '''
            start_square, end_square = self.game.index_dict[action]

            # 50 move rule
            # print("Action: ", a)
            # display(canonicalBoard)
            if abs(board[start_square[0]][start_square[1]]) == 1:
                # print(abs(canonicalBoard[start_square[0]][start_square[1]]))
                moves_no_progress = 0
            elif board[end_square[0]][end_square[1]] != 0:
                # print(canonicalBoard[end_square[0]][end_square[1]])
                moves_no_progress = 0
            else:
                moves_no_progress += 1

            if moves_no_progress >= 100:
                return 1e-8


            # 3 fold repetition
            board_string = self.game.stringRepresentation(board)
            if board_string in seen_positions:
                seen_positions[board_string] += 1
                if seen_positions[board_string] >= 3:
                    return 1e-8
            else:
                seen_positions[board_string] = 1
            '''

            board, curPlayer = self.game.getNextState(board, curPlayer, action)

        if verbose:
            assert(self.display)
            print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board, 1)))
            self.display(board)
        return self.game.getGameEnded(board, 1)

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """
        eps_time = AverageMeter()
        bar = Bar('Arena.playGames', max=num)
        end = time.time()
        eps = 0
        maxeps = int(num)

        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1
            # bookkeeping + plot progress
            eps += 1
            eps_time.update(time.time() - end)
            end = time.time()
            bar.suffix = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps + 1, maxeps=maxeps, et=eps_time.avg,
                                                                                                       total=bar.elapsed_td, eta=bar.eta_td)
            bar.next()

        self.player1, self.player2 = self.player2, self.player1

        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1
            # bookkeeping + plot progress
            eps += 1
            eps_time.update(time.time() - end)
            end = time.time()
            bar.suffix = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps + 1, maxeps=num, et=eps_time.avg,
                                                                                                       total=bar.elapsed_td, eta=bar.eta_td)
            bar.next()

        bar.finish()

        return oneWon, twoWon, draws
