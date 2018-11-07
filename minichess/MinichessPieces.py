# All pieces will be their own class
# Color and movements will be stored in each class

# Hard coded dimensions 5 x 5 - Gardner chess


class Piece():
    def __init__(self, color):
        self.color = color

# In all classes, get moves will return a list of tuples of tuples.
# Ex ((1, 2), (2, 2)) represents moving the piece at (1, 2) to (2, 2)

class Pawn(Piece):
    # define col = 1 when white, col = -1 when black
    # row and col are the coordinates for the square the pawn is currently on
    # row and col are indexed at 0
    def __init__(self, color):
        self.start_row = 1 if color == "white" else 3
        self.direction = 1 if self.start_row == 1 else -1
        self.name = "wp" if color == "white" else "bp"
        super().__init__(color)

    # Passes in board as a list of lists containing the 
    # Note: pawns can only move forward one square
    def get_moves(self, board, row, col):

        # will be a list of tuples 
        moves = []

        # Check if we can move it forward one row
        if board[row + self.direction][col] == 0:
            moves.append( ((row, col), (row + 1, col)) )

        # Test the diagonals. Pawns can only move (one) square
        # diagonally if there is a piece to take.
        left_diagonal = board.at(x + move_dir, y - 1)
        right_diagonal = board.at(x + move_dir, y + 1)

        def opponent_piece_exists(square):
            if not square.is_empty():
                return (square != InvalidSquare() and
                        square.piece.color != self.colour)
            return False

        if opponent_piece_exists(left_diagonal):
            moves.append(left_diagonal)
        if opponent_piece_exists(right_diagonal):
            moves.append(right_diagonal)

        return moves

    def __str__(self):
        return(self.name)


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, board, row, col):
        pass

    def __str__(self):
        return("N")


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, board, row, col):
        pass

    def __str__(self):
        return("B")


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, board, row, col):
        pass

    def __str__(self):
        return("R")


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, board, row, col):
        pass

    def __str__(self):
        return("Q")


class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_moves(self, board, row, col):
        pass

    def __str__(self):
        return("K")


# test = Pawn(color="black")
# print(test.color)
# print(test.start_row)
# print(test.direction)
# print(type(test).__name__)


'''
class Knight(Piece):

    def __init__(self, colour):
        super(Knight, self).__init__(colour)

    def enumerate_moves(self, board, x, y):
        indices = [board.at(x + 2, y + 1),
                   board.at(x + 2, y - 1),
                   board.at(x + 1, y + 2),
                   board.at(x + 1, y - 2),
                   board.at(x - 1, y + 2),
                   board.at(x - 1, y - 2),
                   board.at(x + 2, y + 1),
                   board.at(x + 2, y - 1)]

        return [square for square in indices if
                square != InvalidSquare()]

    def __str__(self):
        return 'N'


class Bishop(Piece):

    def __init__(self, colour):
        super(Bishop, self).__init__(colour)

    def enumerate_moves(self, board, x, y):

        def not_invalid(square):
            return square.can_move_to(self)

        positive = takewhile(not_invalid,
                             (board.at(x + n, y + n) for n in board_size[1:]))
        negative = takewhile(not_invalid,
                             (board.at(x - n, y - n) for n in board_size[1:]))
        pos_neg = takewhile(not_invalid,
                            (board.at(x + n, y - n) for n in board_size[1:]))
        neg_pos = takewhile(not_invalid,
                            (board.at(x - n, y + n) for n in board_size[1:]))

        return list(chain(positive, negative, pos_neg, neg_pos))

    def __str__(self):
        return 'B'


class Rook(Piece):

    def __init__(self, colour):
        super(Rook, self).__init__(colour)

    def enumerate_moves(self, board, x, y):

        def not_invalid(square):
            return square.can_move_to(self)

        x_positive = takewhile(not_invalid,
                               (board.at(x + n, y) for n in board_size[1:]))
        x_negative = takewhile(not_invalid,
                               (board.at(x - n, y) for n in board_size[1:]))
        y_positive = takewhile(not_invalid,
                               (board.at(x, y + n) for n in board_size[1:]))
        y_negative = takewhile(not_invalid,
                               (board.at(x, y - n) for n in board_size[1:]))

        return list(chain(x_positive, x_negative, y_positive, y_negative))

    def __str__(self):
        return 'R'


class Queen(Piece):

    def __init__(self, colour):
        super(Queen, self).__init__(colour)

    def enumerate_moves(self, board, x, y):
        # Moves for a queen are the union of those from a rook
        # and a bishop.
        bishop = Bishop(self.colour)
        rook = Rook(self.colour)

        bishop_moves = bishop.enumerate_moves(board, x, y)
        rook_moves = rook.enumerate_moves(board, x, y)
        bishop_moves.extend(rook_moves)
        return bishop_moves

    def __str__(self):
        return 'Q'


class King(Piece):

    def __init(self, colour):
        super(King, self).__init__(colour)

    def enumerate_moves(self, board, x, y):
        indices = [board.at(x + 1, y),
                   board.at(x - 1, y),
                   board.at(x, y + 1),
                   board.at(x, y - 1),
                   board.at(x - 1, y + 1),
                   board.at(x - 1, y - 1),
                   board.at(x + 1, y + 1),
                   board.at(x + 1, y - 1)]

        return [square for square in indices if square != InvalidSquare()]

    def __str__(self):
        return 'K'
'''
