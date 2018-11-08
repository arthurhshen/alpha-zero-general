import numpy as np

dim = (5, 5)


board = [None] * dim[0]
for i in range(dim[0]):
    # board[i] = [0] * dim[0]
    if (i == 0):
        # Create all the white pieces here: R, N, B, Q, K
        board[i] = [4, 2, 3, 5, 6]
    elif (i == 1):
        board[i] = [1] * dim[1]
    elif (i == dim[0] - 2):
        board[i] = [-1] * dim[1]
    elif (i == dim[0] - 1):
        board[i] = [-4, -2, -3, -5, -6]
        # Create all the white pieces here: R, N, B, Q, K
    else:
        board[i] = [0] * dim[1]

board = np.array(board)
# print(board)

print(board)

board = np.flip(board, 0) * -1

print(board)

# deep copy
new_board = np.copy(board)

promotions = [2, 3, 4, 5, None]

print(promotions)

test_set1 = {'a', 'b'}
test_set2 = set()

print(test_set2 | test_set1)

elements = {(1, 1, 1), (2, 3, 7), (3, 5, 10)}

print((1, 1, 1) in elements)

print(set([x[1] for x in elements]))
