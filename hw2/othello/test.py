"""
COMS W4701 Artificial Intelligence - Programming Homework 2

This module contains functions that are accessed by the game manager
and by the each AI player. Feel free to call these functions when
building your AIs.

@author: Daniel Bauer
"""
#import sys;

test_dict = {};

def get_score(board):
    p1_count = 0
    p2_count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                p1_count += 1
            elif board[i][j] == 2:
                p2_count += 1
    return p1_count, p2_count


board = []
for i in range(4):
    row = []
    for j in range(4):
        row.append(0)
    board.append(row)

i = 4 // 2 -1
j = 4 // 2 -1
board[i][j] = 2
board[i+1][j+1] = 2
board[i+1][j] = 1
board[i][j+1] = 1

final = []
for row in board:
    final.append(tuple(row))

def compute_utility(board, color):
    black, white = get_score(board);
    if color == 1:
        return black - white;
    else:
        return white - black;

#print ("--------");
#print (compute_utility(board,2));

#print(board);
#board = (tuple)board;
#print(type(board));
#test_dict['0'] = 00;
#test_dict['1'] = 11;
print (test_dict);
