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
    Sw = blocked_pawns(board,'white')
    Sb = blocked_pawns(board,'black')
    Iw = isolated_pawns(board,'white')
    Ib = isolated_pawns(board,'black')
    Adv_pawn_w =advanced_pawns(board,'white')
    Adv_pawn_b = advanced_pawns(board, 'black')
    bp=bishop_pair(board)

    #Calculating the evaluation using the weights. The weights here are given by hand.
    evaluation1 = 900*(Qw - Qb) + 500*(Rw - Rb) +330*(Bw-Bb
                )+320*(Nw - Nb) +100*(Pw - Pb) +-30*(Dw-Db + Sw-Sb + Iw- Ib
                )+300*(Adv_pawn_w-Adv_pawn_b)+30*bp
    #Evaluation of piece square tables:
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

    score = 0

    for i in range(64):
        if flatboard[i]==0:
            continue

        piece = flatboard[i][0]
        colour = flatboard[i][1]
        sign = +1

        if colour=='b':
            i = int((7-i/8)*8 + i%8)
            sign = -1
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
            if gamephase=='opening':
                score+=sign*king_table[i]
            else:
                score+=sign*king_endgame_table[i]
    return score

def doubledPawns(board,colour):
    '''' This function counts the number of doubled pawns for a player and returns it.
    Doubled pawns are those that are on the same file.

    Args:
        board: current board state.
        colour:  white or black????

    Returns:
        It returnes the number of doubled pawns.
    '''

    colour = colour[0]

    list_of_pawns = look_for(board,'P'+colour)
    reps = 0
    temp = []
    for pawn_pos in list_of_pawns:
        if pawn_pos[0] in temp:
            reps = reps + 1
        else:
            temp.append(pawn_pos[0])
    return reps


def blocked_pawns(board,colour):
    '''' This function counts the number of blocked pawns for a player and returns it.
    Blocked pawns are those that have a piece in front of them and so cannot advance forward.

    Args:
        board: current board state.
        colour:  white or black????

    Returns:
        It returnes the number of blocked pawns.
    '''

    colour = colour[0]
    list_of_pawns = look_for(board,'P'+colour)
    blocked = 0

    for pawn_pos in list_of_pawns:
        if ((colour=='w' and is_occupied_by(board,pawn_pos[0],pawn_pos[1]-1,
                                       'black'))
            or (colour=='b' and is_occupied_by(board,pawn_pos[0],pawn_pos[1]+1,
                                       'white'))):
            blocked = blocked + 1
    return blocked



def isolated_pawns(board,colour):
    ''''  This function counts the number of isolated pawns for a player. These are pawns
    that do not have supporting pawns on adjacent files and so are difficult to protect.

    Args:
        board: current board state.
        colour:  white or black????

    Returns:
        It returnes the number of isolated pawns.
    '''

    colour = colour[0]
    list_of_pawns = look_for(board,'P'+colour)
    x_list = [x for (x,y) in list_of_pawns]
    isolated = 0
    for x in x_list:
        if x!=0 and x!=7:

            if x-1 not in x_list and x+1 not in x_list:
                isolated+=1
        elif x==0 and 1 not in x_list:
            isolated+=1
        elif x==7 and 6 not in x_list:
            
            isolated+=1
    return isolated

def advanced_pawns(board,colour):
    advanced_pawn_mul = 40
    promotable_bonus = 350
    score = 0
    list_of_pawns = look_for(board, 'P' + colour)
    for piece in list_of_pawns:
        if piece.colour == 'white':
            if piece.y >= 4:
                score += piece.y * advanced_pawn_mul
            if piece.is_promotable:
                score += promotable_bonus
        elif piece.colour == 'black':
            if piece.y <= 3:
                score -= (8 - piece.y) * advanced_pawn_mul
            if piece.is_promotable:
                score -= promotable_bonus
    return score


def knight_on_edge(board,colour):
    knight_on_edge_score = -50
    list_of_knights = look_for(board, 'N' + colour)
    return sum(knight_on_edge_score * (1 if p.colour == 'white' else -1)
               for p in list_of_knights if p.col in 'ah')

def get_pieces(board, colour):

    """
    This function returns a list of positions of all the pieces on the board of a particular colour.
    """
    print('***********')

    list_of_pieces = []
    for j in range(8):
        for i in range(8):
            if is_occupied_by(board, i, j, colour):
                list_of_pieces.append(board[j][i][0])
    return list_of_pieces


def bishop_pair(board):
    bishop_pair_bonus = 50
    white_bishops = look_for(board, 'B' + 'white')
    black_bishops = look_for(board, 'B' + 'black')
    return (bishop_pair_bonus if len(white_bishops) >= 2 else 0
          - bishop_pair_bonus if len(black_bishops) >= 2 else 0)