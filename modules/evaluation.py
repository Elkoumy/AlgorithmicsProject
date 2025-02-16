from modules.chess_ai import  *
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
    look at the positioning of pieces on the chess_board to judge whether white has an advantage or black.

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
        Result = -20000 
        return Result
    if is_check_mate(position,'black'):
        #Major advantage to white
        Result = 20000 
        return Result 

        '''
        getchess_board() from class gamePosition which is should be added
        ??????????????????????????????????????????????????
        '''
    chess_board = position.getchess_board()
    flat_chess_board = [x for row in chess_board for x in row]
    c = Counter(flat_chess_board)
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

    whiteMaterial = 9*Qw + 5*Rw + 3*Nw + 3*Bw + 1*Pw
    blackMaterial = 9*Qb + 5*Rb + 3*Nb + 3*Bb + 1*Pb
    '''
    get_history() from class gamePosition which is should be added
    ??????????????????????????????????????????????????
    '''
    numofmoves = len(position.get_history())

    phase = 'opening'
    if numofmoves>40 or (whiteMaterial<14 and blackMaterial<14):
        phase = 'ending'
    
    Dw = doubled_pawns(chess_board,'white')
    Db = doubled_pawns(chess_board,'black')
    Sw = blocked_pawns(chess_board,'white')
    Sb = blocked_pawns(chess_board,'black')
    Iw = isolated_pawns(chess_board,'white')
    Ib = isolated_pawns(chess_board,'black')
    Adv_pawn_w =advanced_pawns(chess_board,'white')
    Adv_pawn_b = advanced_pawns(chess_board, 'black')
    bp=bishop_pair(chess_board)

    #Calculating the evaluation using the weights. The weights here are given by hand.
    eval1 = 900*(Qw - Qb) + 500*(Rw - Rb) +330*(Bw-Bb
                )+320*(Nw - Nb) +100*(Pw - Pb) +-30*(Dw-Db + Sw-Sb + Iw- Ib
                )+300*(Adv_pawn_w-Adv_pawn_b)+30*bp
    #Evaluation of piece square tables:
    eval2 = piece_square_table(flat_chess_board,phase)
    final_eval = eval1 + eval2
    return final_eval


def piece_square_table(flat_chess_board,phase):
    ''' Gives a position a value  based solely on tables that define points for each position for each piece type

    Args:
        flat_chess_board: a 1D array of the chess_board for faster calculations:
        phase:  Make the AI smarter when analysing chess_boards and has not been

    Returns:
        It returnes the value  of the pieces.
    '''

    value  = 0

    for i in range(64):
        if flat_chess_board[i]==0:
            continue

        piece = flat_chess_board[i][0]
        player_color = flat_chess_board[i][1]
        flag  = +1

        if player_color=='b':
            i = int((7-i/8)*8 + i%8)
            flag  = -1
        if piece=='P':
            value  += flag *pawn_table[i]
        elif piece=='R':
            value +=flag *rook_table[i]
        elif piece=='N':
            value += flag *knight_table[i]
        elif piece=='B':
            value +=flag *bishop_table[i]
        elif piece=='Q':
            value +=flag *queen_table[i]
        elif piece=='K':
            if phase=='opening':
                value +=flag *king_table[i]
            else:
                value +=flag *king_endgame_table[i]
    return value 

def doubled_pawns(chess_board,player_color):
    '''' This function counts the number of doubled pawns for a player and returns it.
    Doubled pawns are those that are on the same file.

    Args:
        chess_board: current chess_board state.
        player_color:  white or black????

    Returns:
        It returnes the number of doubled pawns.
    '''

    player_color = player_color[0]

    list_of_pawns = look_for(chess_board,'P'+player_color)
    reps = 0
    temp = []
    for pawn_pos in list_of_pawns:
        if pawn_pos[0] in temp:
            reps = reps + 1
        else:
            temp.append(pawn_pos[0])
    return reps


def blocked_pawns(chess_board,player_color):
    '''' This function counts the number of blocked pawns for a player and returns it.
    Blocked pawns are those that have a piece in front of them and so cannot advance forward.

    Args:
        chess_board: current chess_board state.
        player_color:  white or black????

    Returns:
        It returnes the number of blocked pawns.
    '''

    player_color = player_color[0]
    list_of_pawns = look_for(chess_board,'P'+player_color)
    blocked = 0

    for pawn_pos in list_of_pawns:
        if ((player_color=='w' and is_occupied_by(chess_board,pawn_pos[0],pawn_pos[1]-1,
                                       'black'))
            or (player_color=='b' and is_occupied_by(chess_board,pawn_pos[0],pawn_pos[1]+1,
                                       'white'))):
            blocked = blocked + 1
    return blocked



def isolated_pawns(chess_board,player_color):
    ''''  This function counts the number of isolated pawns for a player. These are pawns
    that do not have supporting pawns on adjacent files and so are difficult to protect.

    Args:
        chess_board: current chess_board state.
        player_color:  white or black????

    Returns:
        It returnes the number of isolated pawns.
    '''

    player_color = player_color[0]
    list_of_pawns = look_for(chess_board,'P'+player_color)
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

def advanced_pawns(chess_board,player_color):
    advanced_pawn_mul = 40
    promotable_bonus = 350
    value  = 0
    list_of_pawns = look_for(chess_board, 'P' + player_color)
    for piece in list_of_pawns:
        if piece.player_color == 'white':
            if piece.y >= 4:
                value  += piece.y * advanced_pawn_mul
            if piece.is_promotable:
                value  += promotable_bonus
        elif piece.player_color == 'black':
            if piece.y <= 3:
                value  -= (8 - piece.y) * advanced_pawn_mul
            if piece.is_promotable:
                value  -= promotable_bonus
    return value 


def knight_on_edge(chess_board,player_color):
    knight_on_edge_value  = -50
    list_of_knights = look_for(chess_board, 'N' + player_color)
    return sum(knight_on_edge_value  * (1 if p.player_color == 'white' else -1)
               for p in list_of_knights if p.col in 'ah')

def get_pieces(chess_board, player_color):

    """
    This function returns a list of positions of all the pieces on the chess_board of a particular player_color.
    """
    print('***********')

    list_of_pieces = []
    for j in range(8):
        for i in range(8):
            if is_occupied_by(chess_board, i, j, player_color):
                list_of_pieces.append(chess_board[j][i][0])
    return list_of_pieces


def bishop_pair(chess_board):
    bishop_pair_bonus = 50
    white_bishops = look_for(chess_board, 'B' + 'white')
    black_bishops = look_for(chess_board, 'B' + 'black')
    return (bishop_pair_bonus if len(white_bishops) >= 2 else 0
          - bishop_pair_bonus if len(black_bishops) >= 2 else 0)