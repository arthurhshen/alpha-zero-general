'''
# Note: Pawns cannot move 2 squares forward, and therefore there en passant is not a rule.
# There is no castling.

# Possible speed improvements:
# have a variable in Board class "isCheck" that stores a boolean for whether its check and
# the squares between the piece and the king (and the piece putting the king in check.
# When checking for legal moves, pass the possible squares to block with and the square
# the piece is not to see if capturing it is possible. In this way, we can reduce the number
# of illegal moves searched

'''
# from MinichessPieces import *

# used to iterate for bishops/rooks/queens along diagonals/ranks/files until we
# find either a piece of the opposite color, or a piece of our own color.
# from itertools import takewhile

import numpy as np
# For debugging/sleeping
import time


class Board():
    # Pawn = 1, Knight = 2, Bishop = 3, Rook = 4, Queen = 5, King = 6, Empty Square = 0
    # White is positive, black is negative (ex: -4 is a black rook, 3 is a white bishop)

    # pass in tuple of # of rows and # of columns (ranks and files)
    def __init__(self, dim_tuple=(5, 5)):
        self.dim = dim_tuple
        # Create the empty board array of dimensions r x c with pieces.
        # Empty square is 0
        self.board = [None] * self.dim[0]
        for i in range(self.dim[0]):
            # self.board[i] = [0] * self.dim[0]
            if (i == 0):
                # Create all the white pieces here: R, N, B, Q, K
                self.board[i] = [4, 2, 3, 5, 6]
            elif (i == 1):
                self.board[i] = [1] * self.dim[1]
            elif (i == self.dim[0] - 2):
                self.board[i] = [-1] * self.dim[1]
            elif (i == self.dim[0] - 1):
                # Create all the black pieces here: R, N, B, Q, K
                self.board[i] = [-4, -2, -3, -5, -6]
            else:
                # Empty squares
                self.board[i] = [0] * self.dim[1]

                # Set up the initial pieces.

                # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.board[index]

    def make_move(self, move, player):
        # executes 'move' for 'player' and returns the new board - does NOT update self.board
        # print("Move: {}".format(move))
        # print("Type: {}".format(type(move)))

        start_square = move[0]
        end_square = move[1]

        piece = self.board[start_square[0]][start_square[1]]
        # Ensure that the piece being moved is of the correct color/not an empty square

        try:
            assert(piece * player > 0)
        except AssertionError:
            print("Piece: ", piece)
            print("Player: ", player)
            print(self.board)
            print(move)
            time.sleep(100)

        # If the piece is a pawn, we may have to deal with underpromotions
        if abs(piece) == 1:

            # promotion:
            if player == 1:
                if (end_square[0] == self.dim[0] - 1):
                    # promotion defaults to a queen
                    if len(end_square) == 2:
                        piece = 5
                    # underpromtion
                    else:
                        piece = end_square[2]
            # player = -1
            else:
                if (end_square[0] == 0):
                    # promotion default to (black) queen
                    if len(end_square) == 2:
                        piece = -5
                # underpromotion
                    else:
                        piece = end_square[2]

        new_board = np.copy(self.board)
        new_board[end_square[0]][end_square[1]] = piece
        new_board[start_square[0]][start_square[1]] = 0

        return(new_board)

    def get_legal_moves(self, player, check_checks=True):
        """Returns all the legal moves for the given color - .
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.
        rows, cols = self.dim

        for r in range(rows):
            for c in range(cols):
                piece = self.board[r][c]
                if player * piece > 0:
                    moves = moves | self._get_moves_for_piece(r, c, player, check_checks)

        return(moves)

    def _get_moves_for_piece(self, row, col, player, check_checks=True):
        # Note: assume that a new board is created every time we check this, and
        # self.board is updated to contain the new board.

        piece = self.board[row][col]

        if player * piece <= 0:
            return(set())

        # player = 1 if piece > 0 else -1

        piece = abs(piece)
        if piece == 1:
            moves = self._get_moves_for_pawn(row, col, player, check_checks)

        if piece == 2:
            moves = self._get_moves_for_knight(row, col, player, check_checks)

        if piece == 3:
            moves = self._get_moves_for_bishop(row, col, player, check_checks)

        if piece == 4:
            moves = self._get_moves_for_rook(row, col, player, check_checks)

        if piece == 5:
            moves = self._get_moves_for_queen(row, col, player, check_checks)

        if piece == 6:
            moves = self._get_moves_for_king(row, col, player, check_checks)

        return(moves)

    def _check_square(self, orig_row, orig_col, new_row, new_col, player, check_checks=True):
        # Returns True if the player can move a piece to the square
        # (new_row, new_col) and False if the square is occupied by
        # a piece of the same color or is an invalid square
        # Only check for checks

        rows, cols = self.dim
        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
            return(False)

        square = self.board[new_row][new_col]
        if player * square > 0:
            return(False)

        # make sure the position is not check
        new_board = self.make_move(((orig_row, orig_col), (new_row, new_col)), player)
        if check_checks:
            if self._is_check(new_board, player, check_checks=False):
                return(False)

        return(True)

    def _is_check(self, curr_board, player, check_checks=True):
        # Returns true if 'player' is in check
        # Find all squares that the opposite color controls. Also find the
        # square with the 'player' king. If the square with 'player' king
        # is in the set of squares that the opposite color controls, return
        # True

        # create a new board object for the curr_board's position
        temp_b = Board()
        temp_b.board = curr_board

        rows, cols = self.dim
        king_loc = None
        controlled_squares = set(x[1] for x in temp_b.get_legal_moves(-player, check_checks))

        # find king's location
        for r in range(rows):
            for c in range(cols):
                if temp_b.board[r][c] * player == 6:
                    king_loc = (r, c)

        if king_loc in controlled_squares:
            return(True)

        return(False)

    def _get_moves_for_pawn(self, row, col, player, check_checks=True):
        rows, cols = self.dim
        moves = set()
        # promotions
        promotion = False
        if player == 1:
            if row == self.dim[0] - 2:
                promotion = True
                under_promotions = [2, 3, 4, 5]
        else:
            if row == 1:
                promotion = True
                under_promotions = [-2, -3, -4, -5]

        for new_c in range(col - 1, col + 2):
            if new_c < 0 or new_c >= self.dim[1]:
                continue
            # check to see if square is occupied by a piece of the
            # same color
            # Since pawns only move forwards - add player (1 or -1) to row
            new_r = row + player

            # for captures:
            is_piece = True

            if (new_c != col):
                if new_c >= cols or new_c < 0:
                    continue
                if self.board[new_r][new_c] * player >= 0:
                    is_piece = False

            # ensures the square in front of the pawn is empty
            if (new_c == col):
                if self.board[new_r][new_c] != 0:
                    is_piece = False

            if is_piece and self._check_square(row, col, new_r, new_c, player, check_checks):
                moves.add(((row, col), (new_r, new_c)))
                if promotion:
                    for piece in under_promotions:
                        moves.add(((row, col), (new_r, new_c, piece)))

        return(moves)

    def _get_moves_for_knight(self, row, col, player, check_checks=True):
        moves = set()

        new_indices = [
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row - 2, col + 1),
            (row - 2, col - 1),
            (row + 1, col + 2),
            (row + 1, col - 2),
            (row - 1, col + 2),
            (row - 1, col - 2)
        ]

        for new_r, new_c in new_indices:
            if self._check_square(row, col, new_r, new_c, player, check_checks):
                moves.add(((row, col), (new_r, new_c)))

        return(moves)

    def _get_moves_for_bishop(self, row, col, player, check_checks=True):
        moves = set()

        rows, cols = self.dim

        # There's probably a better way of finding these moves - maybe use takewhile
        up_right = True
        up_left = True
        down_right = True
        down_left = True

        for offset in range(1, min(rows, cols)):
            # Up and right diagonal
            if up_right:
                new_r = row + offset
                new_c = col + offset

                if self._check_square(row, col, new_r, new_c, player, check_checks):
                    moves.add(((row, col), (new_r, new_c)))
                    # If the square contains a piece that is captured, then we can no longer
                    # continue on the diagonal, so set up_right = False
                    if self.board[new_r][new_c] != 0:
                        up_right = False
                # Either the diagonal has ended (no longer on the board) or their is a
                # piece of 'player' color in the way
                else:
                    up_right = False

            # Up and left diagonal
            if up_left:
                new_r = row + offset
                new_c = col - offset

                if self._check_square(row, col, new_r, new_c, player, check_checks):
                    moves.add(((row, col), (new_r, new_c)))
                    # If the square contains a piece that is captured, then we can no longer
                    # continue on the diagonal, so set up_right = False
                    if self.board[new_r][new_c] != 0:
                        up_left = False
                # Either the diagonal has ended (no longer on the board) or their is a
                # piece of 'player' color in the way
                else:
                    up_left = False

            if down_right:
                new_r = row - offset
                new_c = col + offset

                if self._check_square(row, col, new_r, new_c, player, check_checks):
                    moves.add(((row, col), (new_r, new_c)))
                    # If the square contains a piece that is captured, then we can no longer
                    # continue on the diagonal, so set up_right = False
                    if self.board[new_r][new_c] != 0:
                        down_right = False
                # Either the diagonal has ended (no longer on the board) or their is a
                # piece of 'player' color in the way
                else:
                    down_right = False

            if down_left:
                new_r = row - offset
                new_c = col - offset

                if self._check_square(row, col, new_r, new_c, player, check_checks):
                    moves.add(((row, col), (new_r, new_c)))
                    # If the square contains a piece that is captured, then we can no longer
                    # continue on the diagonal, so set up_right = False
                    if self.board[new_r][new_c] != 0:
                        down_left = False
                # Either the diagonal has ended (no longer on the board) or there is a
                # piece of 'player' color in the way
                else:
                    down_left = False

        return(moves)

    def _get_moves_for_rook(self, row, col, player, check_checks=True):
        moves = set()
        rows, cols = self.dim

        # There's probably a better way of finding these moves - maybe use takewhile
        up = True
        down = True
        left = True
        right = True

        for offset in range(1, max(rows, cols)):
            if up:
                new_r = row + offset

                if self._check_square(row, col, new_r, col, player, check_checks):
                    moves.add(((row, col), (new_r, col)))
                    if self.board[new_r][col] != 0:
                        # If the square contains a piece that is captured, then we can no longer
                        # continue on the file, so set flag = False
                        up = False
                else:
                    # Either the file has ended (no longer on the board) or there is a
                    # piece of 'player' color in the way
                    up = False
            if down:
                new_r = row - offset

                if self._check_square(row, col, new_r, col, player, check_checks):
                    moves.add(((row, col), (new_r, col)))
                    if self.board[new_r][col] != 0:
                        # If the square contains a piece that is captured, then we can no longer
                        # continue on the file, so set flag = False
                        down = False
                else:
                    # Either the file has ended (no longer on the board) or there is a
                    # piece of 'player' color in the way
                    down = False

            if left:
                new_c = col - offset
                if self._check_square(row, col, row, new_c, player, check_checks):
                    moves.add(((row, col), (row, new_c)))
                    if self.board[row][new_c] != 0:
                        # If the square contains a piece that is captured, then we can no longer
                        # continue on the rank, so set flag = False
                        left = False
                else:
                    # Either the rank has ended (no longer on the board) or there is a
                    # piece of 'player' color in the way
                    left = False

            if right:
                new_c = col + offset
                if self._check_square(row, col, row, new_c, player, check_checks):
                    moves.add(((row, col), (row, new_c)))
                    if self.board[row][new_c] != 0:
                        # If the square contains a piece that is captured, then we can no longer
                        # continue on the diagonal, so set flag = False
                        right = False
                else:
                    # Either the rank has ended (no longer on the board) or there is a
                    # piece of 'player' color in the way
                    right = False

        return(moves)

    def _get_moves_for_queen(self, row, col, player, check_checks=True):
        # Combine bishop and rooks moves
        moves = self._get_moves_for_rook(
            row, col, player, check_checks) | self._get_moves_for_bishop(
            row, col, player, check_checks)

        return(moves)

    def _get_moves_for_king(self, row, col, player, check_checks=True):
        moves = set()

        new_indices = [
            (row + 1, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 0),
            (row - 1, col + 1),
            (row - 1, col - 1),
            (row - 1, col + 0),
            (row + 0, col + 1),
            (row + 0, col - 1)
        ]

        for new_r, new_c in new_indices:
            if self._check_square(row, col, new_r, new_c, player, check_checks):
                moves.add(((row, col), (new_r, new_c)))

        return(moves)


# testBoard = Board((5, 5))
# print(testBoard.board)

# board = testBoard.board

# print(board[1][4])
