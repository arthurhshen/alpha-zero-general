#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: Sejal Jain sj2735
"""

import random
import sys
import time
import numpy as np

# You can use the functions in othello_shared to write your AI
from MinichessLogic import Board
# from MinichessLogic import make_move, get_legal_moves

explored = dict()


def compute_utility(board, player):

    isEnded = getGameEnded(board, player)
    if abs(isEnded) == 1:
        if isEnded == -1:
            return(float('-inf'))
        return(float('inf'))

    # was a draw
    if isEnded != 0:
        return(0)

    # Evaluate the position
    white_mat, black_mat = get_material(board)

    mat_ratio = (white_mat / black_mat - 1) if player == 1 else black_mat / white_mat - 1

    b = Board()
    b.board = np.copy(board)

    # calculates the total number of legal moves for both the player
    # and the opponent
    player_moves = len(b.get_legal_moves(board, player))
    opponent_moves = len(b.get_legal_moves(board, -player))

    move_ratio = player_moves / opponent_moves - 1

    score = mat_ratio * 5 + move_ratio

    return(score)


def getGameEnded(board, player):
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


def get_material(board):
    '''
    Material counts (hand designed)
    pawn: 1
    bishop: 1.5
    knight: 2
    rook: 3
    Queen: 3.5

    pawn = 1
    bishop = 3
    knight = 2
    rook = 4
    queen = 5
    '''

    mat_dict = {1: 1,
                2: 2,
                3: 1.5,
                4: 3,
                5: 5,
                -1: 1,
                -2: 2,
                -3: 1.5,
                -4: 3,
                -5: 5}
    white_count = 0
    black_count = 0

    rows, cols = board.shape

    for r in range(rows):
        for c in range(cols):
            piece = board[r][c]
            print(piece)
            if piece == 0 or abs(piece) == 6:
                continue
            if piece < 0:
                black_count += mat_dict[piece]
            else:
                white_count += mat_dict[piece]

    return((white_count, black_count))

############ ALPHA-BETA PRUNING #####################


def alphabeta_min_node(board, player, alpha, beta, level, limit):
    global explored

    if player == 1:
        opponent = -1
    elif player == -1:
        opponent = 1

    if level >= limit:
        return compute_utility(board, player)

    else:
        level = level + 1

    if (board, opponent) in explored:
        return explored[(board, opponent)]

    b = Board()
    b.board = np.copy(board)

    moves = b.get_legal_moves(player)

    if len(moves) == 0:
        ans = compute_utility(board, player)
        return ans

    v = float("inf")
    # sort moves based on associated utility value for result board
    moves.sort(key=lambda x: compute_utility(b.make_move(board, player)[0], player))

    for move in moves:
        state, _ = board.make_move(move, opponent)
        if (state, opponent) in explored:
            val = explored[(state, opponent)]
        else:
            val = alphabeta_max_node(state, player, alpha, beta, level, limit)
            explored[(state, opponent)] = val

        v = min(v, val)
        if v <= alpha:
            return v

        beta = min(beta, v)

    return v


def alphabeta_max_node(board, player, alpha, beta, level, limit):
    global explored

    if level >= limit:
        return compute_utility(board, player)
    else:
        level = level + 1

    if (board, player) in explored:
        return explored[(board, player)]

    b = Board()
    b.board = np.copy(board)

    moves = b.get_legal_moves(player)
    if len(moves) == 0:
        ans = compute_utility(board, player)
        return ans

    v = float("-inf")
    # sort moves based on associated utility value for result board
    moves.sort(key=lambda x: compute_utility(b.make_move(board, player)[0], player), reverse=True)

    for move in moves:
        state, _ = board.make_move(move, player)
        if (state, player) in explored:
            val = explored[(state, player)]
        else:
            val = alphabeta_min_node(state, player, alpha, beta, level, limit)
            explored[(state, player)] = val

        v = max(v, val)

        if v >= beta:
            return v

        alpha = max(alpha, v)
    return v


def select_move_alphabeta(board, player):
    global explored

    b = Board()
    b.board = np.copy(board)

    selected_move = -1
    moves = b.get_legal_moves(player)

    minimax_val = float("-inf")

    # sort moves based on associated utility value for result board
    moves.sort(key=lambda x: compute_utility(b.make_move(board, player)[0], player), reverse=True)

    for move in moves:
        state, _ = b.make_move(move, player)
        if (state, player) in explored:
            u = explored[(state, player)]
        else:
            u = alphabeta_min_node(state, player, float("-inf"), float("inf"), 0, 10)
            explored[(state, player)] = u
        if u > minimax_val:
            minimax_val = u
            selected_move = move
    return selected_move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            movei, movej = select_move_alphabeta(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    # run_ai()
    b = Board()
    print(compute_utility(b.board, 1))
