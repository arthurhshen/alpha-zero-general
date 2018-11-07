'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.


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


class Board():

    # Pawn = 1, Knight = 2, Bishop = 3, Rook = 4, Queen = 5, King = 6, Empty Square = 0
    # White is positive, black is negative (ex: -4 is a black rook, 3 is a white bishop)

    # Directions for movement
    # list of all 8 directions on the board, as (x,y) offsets
    # __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    # pass in tuple of # of rows and # of columns (ranks and files)
    def __init__(self, dim_tuple):
        # Intializes configuration

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
                self.board[i] = [-4, -2, -3, -5, -6]
                # Create all the white pieces here: R, N, B, Q, K
            else:
                self.board[i] = [0] * self.dim[1]

                # Set up the initial pieces.

                # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.board[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

    def has_legal_moves(self, color):
        pass

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white pieces, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """
        pass

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        # Much like move generation, start at the new piece's square and
        # follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        pass

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin
        color = self[x][y]
        flips = []

        for x, y in Board._increment_move(origin, direction, self.n):
            if self[x][y] == 0:
                if flips:
                    # print("Found", x,y)
                    return (x, y)
                else:
                    return None
            elif self[x][y] == color:
                return None
            elif self[x][y] == -color:
                # print("Flip",x,y)
                flips.append((x, y))

    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        # initialize variables
        flips = [origin]

        for x, y in Board._increment_move(origin, direction, self.n):
            # print(x,y)
            if self[x][y] == 0:
                return []
            if self[x][y] == -color:
                flips.append((x, y))
            elif self[x][y] == color and len(flips) > 0:
                # print(flips)
                return flips

        return []

    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        #move = (move[0]+direction[0], move[1]+direction[1])
        while all(map(lambda x: 0 <= x < n, move)):
            # while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
            move = list(map(sum, zip(move, direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])


# testBoard = Board((5, 5))
# print(testBoard.board)

# board = testBoard.board

# print(board[1][4])
