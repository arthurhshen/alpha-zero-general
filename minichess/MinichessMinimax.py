#!/usr/bin/env python3
# -*- coding: utf-8 -*


import random
import sys
import time
import numpy as np
import time

# You can use the functions in othello_shared to write your AI
from .MinichessLogic import Board
# from MinichessLogic import make_move, get_legal_moves
explored = dict()
count = 0


class MinimaxPlayer():

    def __init__(self, game, player):
        self.game = game
        self.player = player
        # self.explored = dict()
 
    def compute_utility(self, board, player):
        # print("compute_utility")
        # print(board)
        # print(player)

        curr_board = np.copy(board.reshape(10, 5, 5)[0])

        isEnded = self.game.getGameEnded(board, player)
        if abs(isEnded) == 1:
            if isEnded == -1:
                return(float(-100000))
            return(float(100000))

        # was a draw
        if isEnded != 0:
            return(0)

        # Evaluate the position
        white_mat, black_mat = self.get_material(curr_board)

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

    def min_node(self, board, player, alpha, beta, level, limit):
        global count
        global explored

        if level >= limit:
            return self.compute_utility(board, player)
        else:
            level = level + 1

        if (board.tostring(), player) in explored:
            return explored[(board, tostring(), player)]

        else:
            if player == 1:
                opponent = -1
            elif player == -1:
                opponent = 1
            b = Board()
            b.board = np.copy(board)
            moves = list(b.get_legal_moves(opponent))

            if len(moves) == 0:
                return self.compute_utility(b.board, player)

            if len(moves) > 5:
                moves = moves[0:5]

            next_states = []
            for move in moves:
                next_states.append(player * self.compute_utility(b.make_move(move, opponent), player))

            # sorted moves by utility, takes into account which player it is from above line
            indexes = list(range(len(next_states)))
            indexes.sort(key=next_states.__getitem__)
            moves = list(map(moves.__getitem__, indexes))

            selected_move = -1
            min_val = float("inf")

            for move in moves:
                state = b.make_move(move, opponent)
                count += 1

                if (state.tostring(), player) in explored:
                    u = explored[(state.tostring(), player)]
                else:
                    u = self.max_node(state, player, alpha, beta, level, 5)
                    explored[(state.tostring(), player)] = u

                min_val = min(u, min_val)
                if min_val <= alpha:
                    return min_val

                beta = min(beta, min_val)

            return min_val

    def max_node(self, board, player, alpha, beta, level, limit):
        global count
        global explored

        if level >= limit:
            return self.compute_utility(board, player)
        else:
            level = level + 1

        if (board.tostring(), player) in explored:
            return explored[(board, tostring(), player)]

        else:
            b = Board()
            b.board = np.copy(board)
            moves = list(b.get_legal_moves(player))

            if len(moves) == 0:
                return self.compute_utility(b.board, player)

            if len(moves) > 5:
                moves = moves[0:5]

            next_states = []

            for move in moves:
                next_states.append(player * self.compute_utility(b.make_move(move, player), player))

            # sorted moves by utility, takes into account which player it is from above line
            indexes = list(range(len(next_states)))
            indexes.sort(key=next_states.__getitem__)
            moves = list(map(moves.__getitem__, indexes))

            selected_move = -1
            max_val = float("-inf")

            for move in moves:
                state = b.make_move(move, player)
                count += 1

                if (state.tostring(), player) in explored:
                    u = explored[(state.tostring(), player)]
                else:
                    u = self.min_node(state, player, alpha, beta, level, 5)
                    explored[(state.tostring(), player)] = u

                max_val = max(max_val, u)
                if max_val >= beta:
                    return max_val

                alpha = max(alpha, max_val)

            return max_val

    def select_move(self, board):
        global explored
        global count

        start_time = time.time()

        player = self.player
        b = Board()
        b.board = np.copy(board)

        moves = list(b.get_legal_moves(player))
        if len(moves) > 5:
            moves = moves[0:5]
        next_states = []
        for move in moves:
            next_states.append(player * self.compute_utility(b.make_move(move, player), player))
        # print(moves)
        # print(next_states)
        # sorted moves by utility, takes into account which player it is from above line
        indexes = list(range(len(next_states)))
        indexes.sort(key=next_states.__getitem__)
        moves = list(map(moves.__getitem__, indexes))
        # print(moves)
        selected_move = -1
        minimax_val = float("-inf")

        # iterate through moves
        for move in moves:
            state = b.make_move(move, player)
            count += 1

            if (state.tostring(), player) in explored:
                u = explored[(state.tostring(), player)]
            else:
                u = self.min_node(state, player, float("-inf"), float("inf"), 0, 5)
                explored[(state.tostring(), player)] = u
            if u > minimax_val:
                minimax_val = u
                selected_move = move

        end_time = time.time()

        print("Selected move: ", selected_move)
        print("Total explored positions: ", count)
        print("Time: ", end_time - start_time)

        index = self.game.action_dict[selected_move]
        explored = dict()

        return index
