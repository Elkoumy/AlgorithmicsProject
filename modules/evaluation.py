"""
The evaluation function is to perform the evaluation used by the AI negamax algorithm to evaluate possible movements
El Koumy
8/1/2020
"""
from modules.chess_processing import *
from classes import *
from modules.chess_ai import  *
from collections import defaultdict
from collections import Counter

pawn_table = [  0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]
knight_table = [-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-90,-30,-30,-30,-30,-90,-50]
bishop_table = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-90,-10,-10,-90,-10,-20]
rook_table = [0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]
queen_table = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, 70, -5,-10,-10,-20]
king_table = [-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20]
king_endgame_table = [-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50]


def evaluate(position):
    ''' This function takes as input a position to be analysed.  It will
    look at the positioning of pieces on the board to judge whether white has an advantage or black.

    Args:
        position: current place for chess piece.

    Returns:
        It returnes the evaluation of the pieces and has three different values as below:
        1. Zero: it means it considers the position to be equal for both sides.
        2. +ve: A positive value is an advantage to the white side.
        3. -ve: A negative value is an advantage to the black side.
    '''


    if is_check_mate(position,'white'):
        #Major advantage to black
        return -20000
    if is_check_mate(position,'black'):
        #Major advantage to white
        return 20000

        '''
        getboard() from class gamePosition which is should be added
        ??????????????????????????????????????????????????
        '''
    #Get the board:
    board = position.getboard()
    #Flatten the board to a 1D array for faster calculations:
    flatboard = [x for row in board for x in row]
    #Create a counter object to count number of each pieces:
    c = Counter(flatboard)
    Qw = c['Qw']
    Qb = c['Qb']
    Rw = c['Rw']
    Rb = c['Rb']
    Bw = c['Bw']
    Bb = c['Bb']
    Nw = c['Nw']
    Nb = c['Nb']
    Pw = c['Pw']
    Pb = c['Pb']
    #Note: The above choices to flatten the board and to use a library
    #to count pieces were attempts at making the AI more efficient.
    #Perhaps using a 1D board throughout the entire program is one way
    #to make the code more efficient.
    #Calculate amount of material on both sides and the number of moves
    #played so far in order to determine game phase:
    whiteMaterial = 9*Qw + 5*Rw + 3*Nw + 3*Bw + 1*Pw
    blackMaterial = 9*Qb + 5*Rb + 3*Nb + 3*Bb + 1*Pb
    '''
    gethistory() from class gamePosition which is should be added
    ??????????????????????????????????????????????????
    '''
    numofmoves = len(position.gethistory())

    gamephase = 'opening'
    if numofmoves>40 or (whiteMaterial<14 and blackMaterial<14):
        gamephase = 'ending'
    #A note again: Determining game phase is again one the attempts
    #to make the AI smarter when analysing boards and has not been
    #implemented to its full potential.


    #Calculate number of doubled, blocked, and isolated pawns for
    #both sides:
    Dw = doubledPawns(board,'white')
    Db = doubledPawns(board,'black')
    Sw = blockedPawns(board,'white')
    Sb = blockedPawns(board,'black')
    Iw = isolatedPawns(board,'white')
    Ib = isolatedPawns(board,'black')
    #Evaluate position based on above data:
    evaluation1 = 900*(Qw - Qb) + 500*(Rw - Rb) +330*(Bw-Bb
                )+320*(Nw - Nb) +100*(Pw - Pb) +-30*(Dw-Db + Sw-Sb + Iw- Ib
                )
    #Evaluate position based on piece square tables:
    evaluation2 = pieceSquareTable(flatboard,gamephase)
    #Sum the evaluations:
    evaluation = evaluation1 + evaluation2

    #Return it:
    return evaluation


## this function needs to be modified for more accurate results.
def pieceSquareTable(flatboard,gamephase):
    ''' Gives a position a score based solely on tables that define points for each position for each piece type

    Args:
        flatboard: a 1D array of the board for faster calculations:
        gamephase:  Make the AI smarter when analysing boards and has not been

    Returns:
        It returnes the score of the pieces.
    '''


    #Initialize score:
    score = 0
    #Go through each square:
    for i in range(64):
        if flatboard[i]==0:
            #Empty square
            continue
        #Get data:
        piece = flatboard[i][0]
        color = flatboard[i][1]
        sign = +1
        #Adjust index if black piece, since piece sqaure tables
        #were designed for white:
        if color=='b':
            i = int((7-i/8)*8 + i%8)
            sign = -1
        #Adjust score:
        if piece=='P':
            score += sign*pawn_table[i]
        elif piece=='N':
            score+= sign*knight_table[i]
        elif piece=='B':
            score+=sign*bishop_table[i]
        elif piece=='R':
            score+=sign*rook_table[i]
        elif piece=='Q':
            score+=sign*queen_table[i]
        elif piece=='K':
            #King has different table values based on phase
            #of the game:
            if gamephase=='opening':
                score+=sign*king_table[i]
            else:
                score+=sign*king_endgame_table[i]
    return score



# isolatedPawns(board,color) - This function counts the number of isolated pawns
# for a player. These are pawns that do not have supporting pawns on adjacent files
# and so are difficult to protect.
#
#


def doubledPawns(board,color):
    '''' This function counts the number of doubled pawns for a player and returns it.
    Doubled pawns are those that are on the same file.

    Args:
        board: current board state.
        color:  white or black????

    Returns:
        It returnes the number of doubled pawns.
    '''

    color = color[0]
    #Get indices of pawns:
    listofpawns = look_for(board,'P'+color)
    #Count the number of doubled pawns by counting occurences of
    #repeats in their x-coordinates:
    repeats = 0
    temp = []
    for pawnpos in listofpawns:
        if pawnpos[0] in temp:
            repeats = repeats + 1
        else:
            temp.append(pawnpos[0])
    return repeats


def blockedPawns(board,color):
    '''' This function counts the number of blocked pawns for a player and returns it.
    Blocked pawns are those that have a piece in front of them and so cannot advance forward.

    Args:
        board: current board state.
        color:  white or black????

    Returns:
        It returnes the number of blocked pawns.
    '''

    color = color[0]
    listofpawns = look_for(board,'P'+color)
    blocked = 0
    #Self explanatory:
    for pawnpos in listofpawns:
        if ((color=='w' and is_occupied_by(board,pawnpos[0],pawnpos[1]-1,
                                       'black'))
            or (color=='b' and is_occupied_by(board,pawnpos[0],pawnpos[1]+1,
                                       'white'))):
            blocked = blocked + 1
    return blocked



def isolatedPawns(board,color):
    ''''  This function counts the number of isolated pawns for a player. These are pawns
    that do not have supporting pawns on adjacent files and so are difficult to protect.

    Args:
        board: current board state.
        color:  white or black????

    Returns:
        It returnes the number of isolated pawns.
    '''

    color = color[0]
    listofpawns = look_for(board,'P'+color)
    #Get x coordinates of all the pawns:
    xlist = [x for (x,y) in listofpawns]
    isolated = 0
    for x in xlist:
        if x!=0 and x!=7:
            #For non-edge cases:
            if x-1 not in xlist and x+1 not in xlist:
                isolated+=1
        elif x==0 and 1 not in xlist:
            #Left edge:
            isolated+=1
        elif x==7 and 6 not in xlist:
            #Right edge:
            isolated+=1
    return isolated
