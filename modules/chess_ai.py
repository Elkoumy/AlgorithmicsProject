'''
In this file, we are going to implement the chess ai functions.
Kamel
2/1/2020
'''

from classes import *
#from modules import chess_processing


# all_moves()
# import all_moves from Gamal's code
#from modules.chess_processing import all_moves as allMoves

# make_move()
# import make_move from Gamal's code
#from modules.chess_processing import make_move as makemove

#pos_to_key()
# import pos_to_key from Gamal's code
#from modules.chess_processing import pos_to_key as pos2key

# is_check_mate()
# import isCheckmate from Gamal's code
#from modules.chess_processing import is_check_mate as isCheckmate


###########################////////AI RELATED FUNCTIONS\\\\\\\\\\############################

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
    #
    if root:
        #Generate key from current position:
        key = pos_to_key(position)
        if key in openings:
            #Return the best move to be played:
            bestMoveReturn[:] = random.choice(openings[key])
            return

    # Access global variable that will store scores of positions already evaluated:
    global searched

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
    listofpawns = lookfor(board,'P'+color)
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
    listofpawns = lookfor(board,'P'+color)
    blocked = 0
    #Self explanatory:
    for pawnpos in listofpawns:
        if ((color=='w' and isOccupiedby(board,pawnpos[0],pawnpos[1]-1,
                                       'black'))
            or (color=='b' and isOccupiedby(board,pawnpos[0],pawnpos[1]+1,
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
    listofpawns = lookfor(board,'P'+color)
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
