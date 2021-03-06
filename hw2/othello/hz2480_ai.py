#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: Huibo Zhao hz2480
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
from heapq import heappush
from heapq import heappop

####### dictionary ##########
minimax_dict = {};
#############################

def compute_utility(board, color):
    black, white = get_score(board);
    if color == 1:
        return black - white;
    else:
        return white - black;


############ MINIMAX ###############################

def minimax_min_node(board, color):
    if (board,color) in minimax_dict:
        return minimax_dict[(board,color)];
    else:
        moves = get_possible_moves(board,color);
        if color == 1:
            opponent_color = 2;
        else:
            opponent_color = 1;

        if len(moves)==0: #terminal state
            utility = compute_utility(board,opponent_color);
            minimax_dict[(board,color)] = utility;
            return utility;
        else:
            scores = [];
            for move in moves:
                scores.append(minimax_max_node
                (play_move(board, color, move[0],move[1]),opponent_color));
        minimumScore = min(scores);
        minimax_dict[(board,color)] = minimumScore;
        return minimumScore


def minimax_max_node(board, color):
    if (board,color) in minimax_dict:
        return minimax_dict[(board,color)];
    else:
        moves = get_possible_moves(board,color);
        if color == 1:
            opponent_color = 2;
        else:
            opponent_color = 1;

        if len(moves)==0: #terminal state
            utility = compute_utility(board,color);
            minimax_dict[(board,color)] = utility;
            return utility;
        else:
            scores = [];
            for move in moves:
                scores.append(minimax_min_node
                (play_move(board, color, move[0],move[1]),opponent_color));
        maximumScore = max(scores);
        minimax_dict[(board,color)] = maximumScore;
        return maximumScore


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    if color == 1:
        opponent_color = 2;
    else:
        opponent_color = 1;
    i = 0;
    j = 0;
    maximum = -sys.maxsize;
    #sys.stderr.write("---------------\n");
    moves = get_possible_moves(board,color);
    for move in moves:
        score = minimax_min_node(play_move(board,color,move[0],move[1]),
                                                        opponent_color);
        if score > maximum:
            i, j = move;
            maximum = score;

    return i,j

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    if (board,color) in minimax_dict:
        return minimax_dict[(board,color)];
    else:
        moves = get_possible_moves(board,color);
        if color == 1:
            opponent_color = 2;
        else:
            opponent_color = 1;

        if len(moves)==0: #terminal state
            utility = compute_utility(board,opponent_color);
            minimax_dict[(board,color)] = utility;
            return utility;
        else:
            v = sys.maxsize;
            states = [];
            least_utility = sys.maxsize;
            for move in moves:
                new_board = play_move(board,color,move[0],move[1]);
                heappush(states,(-compute_utility(new_board,opponent_color),new_board));
                least_utility = min(least_utility,compute_utility(new_board,opponent_color));

            if level==limit:
                return least_utility;

            while states:
                new_board = (heappop(states))[1]
                #new_board = play_move(board,color,move[0],move[1]);
                v = min(v,alphabeta_max_node(new_board,opponent_color,alpha,beta,level+1,limit));
                if (v <= alpha):
                    minimax_dict[(board,color)] = v;
                    return v;
                beta = min(beta,v);

            minimax_dict[(board,color)] = v;
            return v


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    if (board,color) in minimax_dict:
        return minimax_dict[(board,color)];
    else:
        moves = get_possible_moves(board,color);
        if color == 1:
            opponent_color = 2;
        else:
            opponent_color = 1;

        if len(moves)==0: #terminal state
            utility = compute_utility(board,color);
            minimax_dict[(board,color)] = utility;
            return utility;
        else:
            v = -sys.maxsize;
            states = [];
            max_utility = -sys.maxsize;
            for move in moves:
                new_board = play_move(board,color,move[0],move[1]);
                heappush(states,(-compute_utility(new_board,color),new_board));
                max_utility = max(max_utility,compute_utility(new_board,color));

            if level==limit:
                return max_utility

            while states:
                new_board = (heappop(states))[1]
                #new_board = play_move(board,color,move[0],move[1]);
                v = max(v,alphabeta_min_node(new_board,opponent_color,alpha,beta,level+1,limit));
                if (v >= beta):
                    minimax_dict[(board,color)] = v;
                    return v;
                alpha = max(alpha,v);

            minimax_dict[(board,color)] = v;
            return v


def select_move_alphabeta(board, color):
    limit_level = 5; # change the limit of the level here
    if color == 1:
        opponent_color = 2;
    else:
        opponent_color = 1;
    i = 0;
    j = 0;
    maximum = -sys.maxsize;

    moves = get_possible_moves(board,color);
    for move in moves:
        score = alphabeta_min_node(play_move(board,color,move[0],move[1]),
                            opponent_color,-sys.maxsize,sys.maxsize,1,limit_level);
        if score > maximum:
            i, j = move;
            maximum = score;

    return i,j


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI") # First line is the name of this AI
    color = int(input()) # Then we read the color: 1 for dark (goes first),
                         # 2 for light.

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
