explored = set()

from MinichessLogic import Board


def alphabeta_min_node(board, color, alpha, beta, level, limit):
    global explored

    if color == 1:
        opponent = 2
    elif color == 2:
        opponent = 1

    if level >= limit:
        return compute_utility(board, color)

    else:
        level = level + 1

    if (board, opponent) in explored:
        return explored[(board, opponent)]

    moves = get_possible_moves(board, opponent)

    if len(moves) == 0:
        ans = compute_utility(board, color)
        return ans

    v = float("inf")

    moves.sort(key=lambda x: compute_utility(play_move(board, color, x[0], x[1]), color))
    for move in moves:
        state = play_move(board, opponent, move[0], move[1])
        if (state, opponent) in explored:
            val = explored[(state, opponent)]
        else:
            val = alphabeta_max_node(state, color, alpha, beta, level, limit)
            explored[(state, opponent)] = val

        v = min(v, val)
        if v <= alpha:
            return v

        beta = min(beta, v)

    return v


def alphabeta_max_node(board, color, alpha, beta, level, limit):
    global explored

    if level >= limit:
        return compute_utility(board, color)
    else:
        level = level + 1

    if (board, color) in explored:
        return explored[(board, color)]

    moves = get_possible_moves(board, color)
    if len(moves) == 0:
        ans = compute_utility(board, color)
        return ans

    v = float("-inf")

    moves.sort(key=lambda x: compute_utility(play_move(board, color, x[0], x[1]), color), reverse=True)
    for move in moves:
        state = play_move(board, color, move[0], move[1])
        if (state, color) in explored:
            val = explored[(state, color)]
        else:
            val = alphabeta_min_node(state, color, alpha, beta, level, limit)
            explored[(state, color)] = val

        v = max(v, val)

        if v >= beta:
            return v

        alpha = max(alpha, v)
    return v


def select_move_alphabeta(board, color):
    global explored

    selected_move = (0, 0)
    moves = get_possible_moves(board, color)

    minimax_val = float("-inf")

    moves.sort(key=lambda x: compute_utility(play_move(board, color, x[0], x[1]), color), reverse=True)
    for move in moves:
        state = play_move(board, color, move[0], move[1])
        if (state, color) in explored:
            u = explored[(state, color)]
        else:
            u = alphabeta_min_node(state, color, float("-inf"), float("inf"), 0, 5)
            explored[(state, color)] = u
        if u > minimax_val:
            minimax_val = u
            selected_move = move
    return selected_move


def compute_utility(board, color):
    pass
