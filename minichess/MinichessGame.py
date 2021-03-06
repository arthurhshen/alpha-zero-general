import sys
# Sets the path to the general alpha-zero folder
sys.path.append('..')
from Game import Game
# from .MinichessLogic import Board
from .MinichessLogic import Board
import numpy as np

# For debugging
import time


class MinichessGame(Game):
    def __init__(self, r, c):
        self.dim = (r, c)

        # Returns action_dict
        def getActionDict():
            # action_dict stores tuples of actions in the form ( (start_square), (end_square) )
            action_dict = {}
            index_dict = {}
            rows, cols = self.dim
            index = 0
            # TODO:
            # If the board size is expanded, add castling and en-passant logic

            for r in range(rows):
                for c in range(cols):
                    # On the given square (r, c), find all possible "queen" moves by finding all rook moves and
                    # bishop moves

                    # Rook moves:

                    # Kingside to queenside moves (left and right)
                    for new_c in range(cols):
                        if new_c == c:
                            continue
                        action_dict[((r, c), (r, new_c))] = index
                        index_dict[index] = ((r, c), (r, new_c))
                        index += 1

                    # Up and down Rook moves
                    for new_r in range(rows):
                        if new_r == r:
                            continue
                        action_dict[((r, c), (new_r, c))] = index
                        index_dict[index] = ((r, c), (new_r, c))
                        index += 1

                    # Bishop moves
                    for new_r in range(rows):
                        # skip original square
                        if new_r == r:
                            continue

                        offset = abs(new_r - r)
                        new_left_c = c - offset
                        new_right_c = c + offset

                        if (new_left_c >= 0):
                            action_dict[((r, c), (new_r, new_left_c))] = index
                            index_dict[index] = ((r, c), (new_r, new_left_c))
                            index += 1
                        if (new_right_c < cols):
                            action_dict[((r, c), (new_r, new_right_c))] = index
                            index_dict[index] = ((r, c), (new_r, new_right_c))
                            index += 1

                    # Knight moves:
                    '''
                    down 2 - left + right
                    up 2 - left + right
                    right 2 - up and down
                    left 2 - up and down
                    '''

                    new_indices = [
                        (r + 2, c + 1),
                        (r + 2, c - 1),
                        (r - 2, c + 1),
                        (r - 2, c - 1),
                        (r + 1, c + 2),
                        (r + 1, c - 2),
                        (r - 1, c + 2),
                        (r - 1, c - 2)
                    ]

                    for new_r, new_c in new_indices:
                        if new_r < 0 or new_r >= rows or new_c < 0 or new_c >= cols:
                            continue
                        action_dict[((r, c), (new_r, new_c))] = index
                        index_dict[index] = ((r, c), (new_r, new_c))
                        index += 1

                    # Add promotions to the action_dict
                    # A promotion is defaulted to Queen
                    # underpromotions are integer representations of the piece -
                    # 4 = Rook, 3 = Bishop, 2 = Knight
                    underpromotions = [5, 4, 3, 2]

                    # White promotion
                    if r == rows - 2:
                        for new_c in range(c - 1, c + 2):
                            if new_c >= 0 and new_c < cols:
                                for piece in underpromotions:
                                    action_dict[((r, c), (rows - 1, new_c, piece))] = index
                                    index_dict[index] = ((r, c), (rows - 1, new_c, piece))
                                    index += 1
                    # Black promotion
                    underpromotions = [-5, -4, -3, -2]
                    if r == 1:
                        for new_c in range(c - 1, c + 2):
                            if new_c >= 0 and new_c < cols:
                                for piece in underpromotions:
                                    action_dict[((r, c), (0, new_c, piece))] = index
                                    index_dict[index] = ((r, c), (0, new_c, piece))
                                    index += 1

            return((action_dict, index_dict))

        self.action_dict, self.index_dict = getActionDict()

        self.action_size = len(self.action_dict)

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.dim)
        return np.array(b.board)

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return(self.dim)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return(self.action_size)

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """

        # Action is in the format ((start square), (end square))
        # Board is a numpy array of the current board state.

        try:
            assert(player == 1)
        except AssertionError:
            print("player: {}".format(player))
            print(self.index_dict[action])
            print(board)
            time.sleep(100)

        b = Board()
        b.board = np.copy(board)

        # in MCTS.py - the action passed in is an integer representing the index of a valid move
        if (isinstance(action, int)):
            action = self.index_dict[action]

        # new_board = b.make_move(action, player)
        # MCTS uses getCanonicalForm - always looks at the board from white's perspective - hard code 1
        new_board = b.make_move(action, player)

        # return(new_board, -player)
        return(new_board, -player)

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board. -- that's not true for
                            chess - we need to reverse the coordinates too
        """
        if player == 1:
            return(board)

        # flips the board so the coordinates are correct (for promotion) and multiplies by -1
        board = np.flip(board, 0) * -1
        return(board)

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    def getSymmetries(self, board, pi):
        # This version of chess is left/right board symmetric (since there is no castling)
        """Board is left/right board symmetric"""
        return [(board, pi), (board[:, ::-1], pi[::-1])]

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """

        # player = 1

        valid_moves = [0] * self.getActionSize()
        b = Board()
        b.board = np.copy(board)

        moves = b.get_legal_moves(player)
        for move in moves:
            valid_moves[self.action_dict[move]] = 1

        return(valid_moves)

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        b = Board()
        b.board = np.copy(board)
        if len(b.get_legal_moves(player)) > 0:
            return(0)
        else:
            # is checkmate
            if (b._is_check(board, player)):
                return(-1)
            # stalemate
            else:
                return(0.0001)


'''

test = MinichessGame(5, 5)

valids = test.getValidMoves(test.getInitBoard(), 1)

count = 0
moves = set()
for v in valids:
    if v == 0:
        count += 1
        continue
    else:
        moves.add(test.index_dict[count])
        count += 1

for m in moves:
    print(m)

test_board = np.array([[], [], [], [], []])

print(test.getInitBoard())

'''
'''
test = MinichessGame(5, 5)
# print(test.action_size)

board, player = test.getNextState(test.getInitBoard(), 1, ((1, 2), (2, 2)))
print(board)
board2, player = test.getNextState(board, -1, ((3, 1), (2, 2)))
print(board2)
board2, _ = test.getNextState(board2, -1, ((2, 2), (1, 1)))
print(board2)
board2, _ = test.getNextState(board2, -1, ((1, 1), (0, 0, -2)))
print(board2)

canonical = test.getCanonicalForm(board2, -1)
print(canonical)


max_index = 0

for key in test.action_dict:
    val = test.action_dict[key]
    if val > max_index:
        max_index = val

    # if key[0] == (0, 1):
    #    print("Val: {}\tGoes to: {}".format(val, key[1]))

# print("max index: {}".format(max_index))
'''
