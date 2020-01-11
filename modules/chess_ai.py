'''
In this file, we are going to implement the chess ai functions.
Kamel
2/1/2020
'''

from classes import *
from collections import Counter #For counting elements in a list effieciently.

#from modules import chess_processing


# all_moves()
#import all_moves from Gamal's code
from modules.chess_processing import all_moves

# make_move()
# import make_move from Gamal's code
from modules.chess_processing import make_move
from modules.chess_processing import *

#pos_to_key()
#import pos_to_key from Gamal's code
from modules.chess_processing import pos_to_key
from collections import defaultdict #Used for giving dictionary values default data types.
from modules.evaluation import *
# is_check_mate()
# import isCheckmate from Gamal's code
#from modules.chess_processing import is_check_mate as isCheckmate
import time
MaxAllowedTimeInSeconds = 30

def negamax(curr_position,depth,alpha,beta,colorsign,bestMoveReturn,root=True):
    ''' generate possible_moves, decide the best move, and use opening table to reduce time.

    Args:
        curr_position: current place for chess piece.
        depth: the depth that search algorithm will look for the next move in.
        alpha and beta: lower and upper bounds to a curr_position's possible
        colorsign: indicates the player to move.
        bestMoveReturn: is a list that will be assigned the move to be played.
        root: s a variable that keeps track of whether the original node is processing now or a lower node.

    Returns:
        best move to be played if we at the root node, else returns the best dict_value.
    '''
    # Scoring of each curr_position is also stored in a global dictionary to allow for time-saving if the same
    # curr_position occurs elsewhere in the tree.
    # First check if the curr_position is already stored in the opening database dictionary:
    startTime = time.time()
    openings_table = defaultdict(list)
    if root:
        dict_key = pos_to_key(curr_position) #Generate dict_key from current curr_position:
        if dict_key in openings_table:
            bestMoveReturn[:] = random.choice(openings_table[dict_key]) #Return the best move to be played:
            return

    global searched  # Access global variable that will store scores of positions already evaluated:
    searched = {}

    if depth==0: #If the depth is zero, we are at a leaf node (no more depth to be analysed):
        return colorsign*evaluate(curr_position)

    possible_moves = all_moves(curr_position, colorsign) #Generate all the possible_moves that can be played:

    if possible_moves==[]: #If there are no possible_moves to be played, just evaluate the curr_position and return it:
        return colorsign*evaluate(curr_position)

    if root: #Initialize a best move for the root node:
        best_move = possible_moves[0]

    best_value = -100000 #Initialize the best move's dict_value:

    for move in possible_moves: #Go through each move:
        newpos = curr_position.clone() #Make a clone of the current move and perform the move on it:
        make_move(newpos,move[0][0],move[0][1],move[1][0],move[1][1])
        dict_key = pos_to_key(newpos)  #Generate the dict_key for the new resulting curr_position:

        if dict_key in searched:  #If this curr_position was already searched before, retrieve its node dict_value, Otherwise, calculate its node dict_value and store it in the dictionary:
            dict_value = searched[dict_key]
            print("Exist")
        elif time.time() - startTime > MaxAllowedTimeInSeconds: 
            print("Time Limit")
            print(depth)
            break
        else:
            dict_value = -negamax(newpos,depth-1, -beta,-alpha,-colorsign,[],False)
            searched[dict_key] = dict_value

        if dict_value>best_value: #If this move is better than the best so far:
            best_value = dict_value
            if root: #If we're at root node, store the move as the best move:
                best_move = move
        alpha = max(alpha,dict_value)  #Update the lower bound for this node:
        if alpha>=beta: #If our lower bound is higher than the upper bound for this node, there #is no need to look at further possible_moves:
            break

    if root: #If this is the root node, return the best move:
        searched = {}
        bestMoveReturn[:] = best_move
        return
    return best_value


