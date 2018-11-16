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
from .MinichessLogic import Board
# from MinichessLogic import make_move, get_legal_moves


class MinimaxPlayer():

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.explored = dict()

    def compute_utility(self, board, player):
        # print("compute_utility")
        # print(board)
        # print(player)
        isEnded = self.getGameEnded(board, player)
        if abs(isEnded) == 1:
            if isEnded == -1:
                return(float(-100000))
            return(float(100000))

        # was a draw
        if isEnded != 0:
            return(0)

        # Evaluate the position
        white_mat, black_mat = self.get_material(board)

        mat_ratio = float('-inf')

        if white_mat == 0:
            mat_ratio = black_mat
        if black_mat == 0:
            mat_ratio = white_mat

        if not mat_ratio >= 0:
            mat_ratio = (white_mat / black_mat - 1) if player == 1 else black_mat / white_mat - 1

        b = Board()
        b.board = np.copy(board)

        # calculates the total number of legal moves for both the player
        # and the opponent
        player_moves = len(b.get_legal_moves(player))
        opponent_moves = len(b.get_legal_moves(-player))

        if opponent_moves == 0:
            move_ratio = player_moves
        else:
            move_ratio = player_moves / opponent_moves - 1

        score = mat_ratio * 2 + move_ratio

        return(score)

    def getGameEnded(self, board, player):
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
        # print("getGameEnded")
        # print(b.board)
        if len(b.get_legal_moves(player)) > 0:
            return(0)
        else:
            # is checkmate
            if (b._is_check(board, player)):
                return(-1)
            # stalemate
            else:
                return(0.0001)

    def get_material(self, board):
        '''
        Material counts (hand designed)
        pawn: 1
        bishop: 1.5
        knight: 2
        rook: 3
        Queen: 4

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
                    5: 6,
                    -1: 1,
                    -2: 2,
                    -3: 1.5,
                    -4: 3,
                    -5: 6}
        white_count = 0
        black_count = 0

        rows, cols = board.shape

        for r in range(rows):
            for c in range(cols):
                piece = board[r][c]
                if piece == 0 or abs(piece) == 6:
                    continue
                if piece < 0:
                    black_count += mat_dict[piece]
                else:
                    white_count += mat_dict[piece]

        return((white_count, black_count))

    ############ ALPHA-BETA PRUNING #####################

    def alphabeta_min_node(self, board, player, alpha, beta, level, limit):
        if player == 1:
            opponent = -1
        elif player == -1:
            opponent = 1

        if level >= limit:
            return self.compute_utility(board, player)

        else:
            level = level + 1

        if (board.tostring(), opponent) in self.explored:
            return self.explored[(board.tostring(), opponent)]

        b = Board()
        b.board = np.copy(board)

        moves = list(b.get_legal_moves(opponent))

        '''
        print("----------------------------------------")
        print("In min_mode, generating possible moves for board for ", opponent)
        print(b.board)
        print(moves)
        print("----------------------------------------")
        '''
        if len(moves) == 0:
            ans = self.compute_utility(board, player)
            return ans

        v = float("inf")
        # sort moves based on associated utility value for result board
        # moves.sort(key=lambda x: self.compute_utility(b.make_move(x, player), player))
        # moves.sort(key=lambda x: self.compute_utility(self.game.getNextState(board, opponent, x)[0], player))

        for move in moves:
            state = b.make_move(move, opponent)
            # state = self.game.getNextState(board, opponent, move)[0]
            if (state.tostring(), opponent) in self.explored:
                val = self.explored[(state.tostring(), opponent)]
            else:
                '''
                print("----------------------------------------")
                print("In min_mode, sending to max_node")
                print(state)
                print(move)
                print("----------------------------------------")
                '''
                val = self.alphabeta_max_node(state, player, alpha, beta, level, limit)
                self.explored[(state.tostring(), opponent)] = val

            v = min(v, val)
            if v <= alpha:
                return v

            beta = min(beta, v)

        return v

    def alphabeta_max_node(self, board, player, alpha, beta, level, limit):
        if level >= limit:
            return self.compute_utility(board, player)
        else:
            level = level + 1

        if (board.tostring(), player) in self.explored:
            return self.explored[(board.tostring(), player)]

        b = Board()
        b.board = np.copy(board)

        moves = list(b.get_legal_moves(player))
        if len(moves) == 0:
            ans = self.compute_utility(board, player)
            return ans

        v = float("-inf")
        # sort moves based on associated utility value for result board
        # moves.sort(key=lambda x: self.compute_utility(b.make_move(x, player), player), reverse=True)
        # moves.sort(key=lambda x: self.compute_utility(self.game.getNextState(board, player, x)[0], player), reverse=True)
        for move in moves:
            # state = b.make_move(move, player)
            # state = self.game.getNextState(board, player, move)[0]
            state = b.make_move(move, player)
            if (state.tostring(), player) in self.explored:
                val = self.explored[(state.tostring(), player)]
            else:
                val = self.alphabeta_min_node(state, player, alpha, beta, level, limit)
                self.explored[(state.tostring(), player)] = val

            v = max(v, val)

            if v >= beta:
                return v

            alpha = max(alpha, v)
        return v

    def select_move_alphabeta(self, board):

        # For our program, the alpha-beta player will always be 1
        player = self.player

        b = Board()
        b.board = np.copy(board)

        # print("in select_move_alphabeta")
        # print(b.board)

        selected_move = -1
        moves = list(b.get_legal_moves(player))
        minimax_val = float("-inf")

        # sort moves based on associated utility value for result board
        # moves.sort(key=lambda x: self.compute_utility(b.make_move(x, player), player), reverse=True)
        # moves.sort(key=lambda x: self.compute_utility(self.game.getNextState(board, player, x)[0], player), reverse=True)
        # print(moves)
        for move in moves:
            # state = b.make_move(move, player)
            # state = self.game.getNextState(board, player, move)[0]
            state = b.make_move(move, player)
            if (state.tostring(), player) in self.explored:
                u = self.explored[(state.tostring(), player)]
            else:
                '''
                print("----------------------------------------")
                print("Sending this state to be evaluated by alphabeta_min_node")
                print(state)
                print("----------------------------------------")
                '''
                u = self.alphabeta_min_node(state, player, float("-inf"), float("inf"), 0, 5)
                self.explored[(state.tostring(), player)] = u
            if u > minimax_val:
                minimax_val = u
                selected_move = move
        print("Selected move: ", selected_move)

        index = self.game.action_dict[selected_move]

        # reset explored set after each move
        print(len(self.explored))
        self.explored = dict()

        return(index)
