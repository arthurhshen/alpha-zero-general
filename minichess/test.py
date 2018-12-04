import numpy as np
from MinichessLogic import Board
from MinichessGame import MinichessGame as Game

'''
row1 = '[[ 0,  0,  0,  0,  6],'
row2 = ' [-4,  0,  0,  0,  0],'
row3 = ' [ 0,  0, -2,  0,  1],'
row4 = ' [ 0, -1,  0,  0, -1],'
row5 = ' [ 0,  0,  0, -5, -6]]'

test = row1 + row2 + row3 + row4 + row5

test = np.array(eval(test))
'''

g = Game(5, 5)

b = Board()

# print(b.board.shape)

# print(b.board.reshape(10, 5, 5)[0])

# test = b.board.reshape(10, 5, 5)

# print(test[0])
# test = test.reshape(50, 5)
# print(test)
print("---------------------------")
# print(b.make_move(((0, 1), (2, 0)), 1).reshape(10, 5, 5))

for i in range(100):

    test = b.make_move(((0, 1), (2, 0)), 1)

    b = Board(new_board=test)
    test = b.make_move(((4, 1), (2, 2)), -1)

    b = Board(new_board=test)
    test = b.make_move(((2, 0), (0, 1)), 1)

    b = Board(new_board=test)
    test = b.make_move(((2, 2), (4, 1)), -1)

    b = Board(new_board=test)


# print(b.board.reshape(10, 5, 5))

orig = b.board.reshape(10, 5, 5)

canonBoard = g.getCanonicalForm(board=b.board, player=-1)

flipped = canonBoard.reshape(10, 5, 5)

print("----------------------------")
# print(canonBoard)

for i in range(10):
    print("----------------------")
    print(orig[i])
    print("**********************")
    print(flipped[i])
    print("----------------------")

# b = Board(b.make_move(((0, 1), (2, 0)), 1))

print(b.fifty_moves())


# print(b.board)
'''
g = Game(5, 5)
print(b.get_legal_moves(1))
print(g.getGameEnded(b.board, 1))


print(g.index_dict[27])
'''
