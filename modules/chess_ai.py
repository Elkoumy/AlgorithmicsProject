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

def negamax(position,depth,alpha,beta,colorsign,bestMoveReturn,root=True):
    ''' generate moves, decide the best move, and use openning table to reduce time.

    Args:
        position: current place for chess piece.
        depth: the depth that search algorithm will look for the next move in.
        alpha and beta: lower and upper bounds to a position's possible
        colorsign: indicates the player to move.
        bestMoveReturn: is a list that will be assigned the move to be played.
        root: s a variable that keeps track of whether the original node is processing now or a lower node.

    Returns:
        best move to be played if we at the root node, else returns the best value.
    '''
    # Scoring of each position is also stored in a global dictionary to allow for time-saving if the same
    # position occurs elsewhere in the tree.

    # First check if the position is already stored in the opening database dictionary:
    startTime = time.time()

    openings = defaultdict(list)
    if root:
        #Generate key from current position:
        key = pos_to_key(position)
        if key in openings:
            #Return the best move to be played:
            bestMoveReturn[:] = random.choice(openings[key])
            return

    # Access global variable that will store scores of positions already evaluated:
    global searched
    searched = {}


    #If the depth is zero, we are at a leaf node (no more depth to be analysed):
    if depth==0:
        return colorsign*evaluate(position)

    #Generate all the moves that can be played:
    moves = all_moves(position, colorsign)

    #If there are no moves to be played, just evaluate the position and return it:
    if moves==[]:
        return colorsign*evaluate(position)

    #Initialize a best move for the root node:
    if root:
        bestMove = moves[0]

    #Initialize the best move's value:
    bestValue = -100000

    #Go through each move:
    for move in moves:
        #Make a clone of the current move and perform the move on it:
        newpos = position.clone()
        make_move(newpos,move[0][0],move[0][1],move[1][0],move[1][1])
        #Generate the key for the new resulting position:
        key = pos_to_key(newpos)
        #If this position was already searched before, retrieve its node value.
        #Otherwise, calculate its node value and store it in the dictionary:
        if key in searched:
            value = searched[key]
            print("Exist")
        elif time.time() - startTime > MaxAllowedTimeInSeconds: 
            print("Time Limit")
            break
        else:
            value = -negamax(newpos,depth-1, -beta,-alpha,-colorsign,[],False)
            searched[key] = value
        #If this move is better than the best so far:
        if value>bestValue:
            #Store it
            bestValue = value
            #If we're at root node, store the move as the best move:
            if root:
                bestMove = move
        #Update the lower bound for this node:
        alpha = max(alpha,value)
        if alpha>=beta:
            #If our lower bound is higher than the upper bound for this node, there
            #is no need to look at further moves:
            break

    #If this is the root node, return the best move:
    if root:
        searched = {}
        bestMoveReturn[:] = bestMove
        return

    #Otherwise, return the bestValue (i.e. value for this node.)
    return bestValue


