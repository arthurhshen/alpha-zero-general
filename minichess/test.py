import numpy as np
from MinichessLogic import Board
from MinichessGame import MinichessGame as Game

row1 = '[[ 0,  0,  0,  0,  6],'
row2 = ' [-4,  0,  0,  0,  0],'
row3 = ' [ 0,  0, -2,  0,  1],'
row4 = ' [ 0, -1,  0,  0, -1],'
row5 = ' [ 0,  0,  0, -5, -6]]'

test = row1 + row2 + row3 + row4 + row5

test = np.array(eval(test))

b = Board()
b.board = test

# print(b.board)

g = Game(5, 5)
print(b.get_legal_moves(1))
print(g.getGameEnded(b.board, 1))


print(g.index_dict[27])


test_dict = {1: 2}

test_dict[1] += 1
print(test_dict)


def test_func(test=dict()):
    print(type(test))


test_func()
test_func(1)

test_list = [1 / 10] * 10
print(test_list)
