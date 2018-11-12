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

# You can use the functions in othello_shared to write your AI
from MinichessLogic import make_move, get_legal_moves

explored = dict()


def compute_utility(board, color):
    score = get_score(board)

    return(utility)

############ ALPHA-BETA PRUNING #####################


def alphabeta_min_node(board, player, alpha, beta, level, limit):
    global explored

    if player == 1:
        opponent = -1
    elif plauyer == -1:
        opponent = 1

    if level >= limit:
        return compute_utility(board, player)

    else:
        level = level + 1

    if (board, opponent) in explored:
        return explored[(board, opponent)]

    moves = board.get_legal_moves(player)

    if len(moves) == 0:
        ans = compute_utility(board, player)
        return ans

    v = float("inf")
    # sort moves based on associated utility value for result board
    moves.sort()
    #moves.sort(key=lambda x:compute_utility(play_move(board, color, x[0], x[1]), color))

    for move in moves:
        state, _ = board.make_move(move, opponent)
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


def alphabeta_max_node(board, player, alpha, beta, level, limit):
    global explored

    if level >= limit:
        return compute_utility(board, player)
    else:
        level = level + 1

    if (board, player) in explored:
        return explored[(board, player)]

    moves = board.get_legal_moves(player)
    if len(moves) == 0:
        ans = compute_utility(board, color)
        return ans

    v = float("-inf")
    # sort moves based on associated utility value for result board
    moves.sort(key=lambda x: compute_utility(board.make_move(board, player), player), reverse=True)

    for move in moves:
        state, _ = board.make_move(move, color)
        if (state, player) in explored:
            val = explored[(state, player)]
        else:
            val = alphabeta_min_node(state, player, alpha, beta, level, limit)
            explored[(state, color)] = val

        v = max(v, val)

        if v >= beta:
            return v

        alpha = max(alpha, v)
    return v


def select_move_alphabeta(board, player):
    global explored

    selected_move = -1
    moves = board.get_legal_moves(player)

    minimax_val = float("-inf")

    # sort moves based on associated utility value for result board
    moves.sort()
    #moves.sort(key=lambda x:compute_utility(make_move(), color), reverse=True)

    for move in moves:
        state, _ = board.make_move(move, player)
        if (state, player) in explored:
            u = explored[(state, player)]
        else:
            u = alphabeta_min_node(state, player, float("-inf"), float("inf"), 0, 10)
            explored[(state, color)] = u
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
    run_ai()
