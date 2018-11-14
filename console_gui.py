# -*- encoding: utf-8 -*-
from minichess.MinichessLogic import Board as board
import os

UNICODE_PIECES = {
  4: u'♜', 2: u'♞', 3: u'♝', 5: u'♛',
  6: u'♚', 1: u'♟', -4: u'♖', -2: u'♘',
  -3: u'♗', -5: u'♕', -6: u'♔', -1: u'♙',
  None: ' '
}


class BoardGuiConsole(object):
    '''
        Print a text-mode chessboard using the unicode chess pieces
    '''
    error = ''

    def __init__(self, chessboard):
        self.board = chessboard

    def move(self):
        os.system("clear")
        self.unicode_representation()
        print("\n", self.error)
        print ("State a move in chess notation (e.g. A2A3). Type \"exit\" to leave:\n", ">>>",)
        self.error = ''
        coord = raw_input()
        if coord == "exit":
            print ("Bye.")
            exit(0)
        try:
            if len(coord) != 4: raise board.InvalidCoord
            self.board.move(coord[0:2], coord[2:4])
            os.system("clear")
        except board.ChessError as error:
            self.error = "Error: %s" % error.__class__.__name__

        self.move()

    def unicode_representation(self):
        #print "\n", ("%s's turn\n" % self.board.player_turn.capitalize()).center(28)
        '''
        for number in self.board.axis_x[::-1]:
            print " " + str(number) + " ",
            for letter in self.board.axis_y:
                piece = self.board[letter+str(number)]
                if piece is not None:
                    print UNICODE_PIECES[piece.abbriviation] + ' ',
                else: print '  ',
            print "\n"
        print "    " + "  ".join(self.board.axis_y)
        '''
        print('   ——   ——   ——   ——   —— ')
        for x in range(self.board.dim[0]):
            for y in range(self.board.dim[1]):
                p = self.board.board[x][y]
                if p != 0:
                    print (' | ' + UNICODE_PIECES[p] + ' ', end='')
                else: print (' |   ', end='')
            print(' |\n   ——   ——   ——   ——   —— ')

                    


def display(board):
    try:
        gui = BoardGuiConsole(board)
        gui.move()
    except (KeyboardInterrupt, EOFError):
        os.system("clear")
        exit(0)