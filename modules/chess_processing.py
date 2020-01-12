'''
In this file, we are going to implement the chess chess_board functions so they could be used by the main module.
El Koumy
31/12/2019

'''

from classes import GamePosition, Shades, Piece
from modules import chess_ai,  GUI


def is_occupied(chess_board, x, y):
    '''
    Returns true if a given coordinate on the chess_board is not empty, and false otherwise.
    '''
    if chess_board[y][x] == 0:
        return False
    return True


def is_occupied_by(chess_board, x, y, color):
    '''
    Only returns true if the square specified by the coordinates is of the specific color inputted.
    '''
    if chess_board[y][x] == 0:
        return False
    if chess_board[y][x][1] == color[0]:
        return True
    return False


def filter_by_color(chess_board, list_of_tuples, color):
    '''
    This function takes the chess_board state, a list of coordinates, and a color as input. It will return the same list,
    but without coordinates that are out of bounds of the chess_board and also without those occupied by the pieces of the
    particular color passed to this function as an argument. In other words, if 'white' is passed in, it will not
    return any white occupied square.
    '''
    filtered_list = []
    for pos in list_of_tuples:
        x = pos[0]
        y = pos[1]
        if x >= 0 and x <= 7 and y >= 0 and y <= 7 and not is_occupied_by(chess_board, x, y, color):

            filtered_list.append(pos)
    return filtered_list


def look_for(chess_board, piece):
    '''
    This functions takes the 2D array that represents a chess_board and finds the indices of all the locations that is
    occupied by the specified piece. The list of indices is returned.
    '''
    list_of_locations = []
    for row in range(8):
        for col in range(8):
            if chess_board[row][col] == piece:
                x = col
                y = row
                list_of_locations.append((x, y))
    return list_of_locations


def is_attacked_by(position, target_x, target_y, color):
    '''
    This function checks if the square specified by (target_x,target_y) coordinates is being attacked by any of a
    specific colored set of pieces.
    '''
    chess_board = position.getchess_board()
    color = color[0]
    list_of_attacked_squares = []
    for x in range(8):
        for y in range(8):
            if chess_board[y][x] != 0 and chess_board[y][x][1] == color:
                list_of_attacked_squares.extend(
                    find_possible_squares(position, x, y, True))  # The true argument

    return (target_x, target_y) in list_of_attacked_squares


def opp(color):
    """
    Returns the complimentary color to the one passed. So inputting 'black' returns 'w', for example.
    """
    color = color[0]
    if color == 'w':
        oppcolor = 'b'
    else:
        oppcolor = 'w'
    return oppcolor


def is_check(position, color):
    """
    This function takes a position as its input and checks if the King of the specified color is under attack by the
    enemy. Returns true if that is the case, and false otherwise.
    """
    chess_board = position.getchess_board()
    color = color[0]
    enemy = opp(color)
    piece = 'K' + color
    x, y = look_for(chess_board, piece)[0]
    return is_attacked_by(position, x, y, enemy)


def is_check_mate(position, color=-1):
    """
    This function tells you if a position is a checkmate. Color is an optional argument that may be passed to
    specifically check for mate against a specific color.
    """
    if color == -1:
        return is_check_mate(position, 'white') or is_check_mate(position, 'b')
    color = color[0]
    if is_check(position, color) and all_moves(position, color) == []:
        return True
    return False


def is_stalemate(position):
    """
    This function checks if a particular position is a stalemate. If it is, it returns true, otherwise it returns false.
    """
    player = position.get_player()
    if player == 0:
        color = 'w'
    else:
        color = 'b'
    if not is_check(position, color) and all_moves(position, color) == []:
        return True
    return False


def get_all_pieces(position, color):
    """
    This function returns a list of positions of all the pieces on the chess_board of a particular color.
    """
    chess_board = position.getchess_board()
    list_of_pos = []
    for j in range(8):
        for i in range(8):
            if is_occupied_by(chess_board, i, j, color):
                list_of_pos.append((i, j))
    return list_of_pos


def all_moves(position, color):
    """
    This function takes as its argument a position and a color/color_sign that represents a side. It generates a list
    of all possible moves for that side and returns it.
    """
    if color == 1:
        color = 'white'
    elif color == -1:
        color = 'black'
    color = color[0]
    list_of_pieces = get_all_pieces(position, color)
    moves = []
    for pos in list_of_pieces:
        targets = find_possible_squares(position, pos[0], pos[1])
        for target in targets:
            moves.append([pos, target])
    return moves


def pos_to_key(position):
    """
    This function takes a position as input argument. For this particular position, it will generate a unique key
    that can be used in a dictionary by making it hashable.
    """
    chess_board = position.getchess_board()
    chess_board_tuple = []
    for row in chess_board:
        chess_board_tuple.append(tuple(row))
    chess_board_tuple = tuple(chess_board_tuple)
    rights = position.getCastleRights()
    tuple_rights = (tuple(rights[0]), tuple(rights[1]))
    key = (chess_board_tuple, position.get_player(),
           tuple_rights)
    return key


def make_move(position, x, y, x2, y2):
    '''
    This function makes a move on the chess_board. The position object gets updated here with new information. (x,y) are
    coordinates of the piece to be moved, and (x2,y2) are coordinates of the destination. (x2,y2) being correct
    destination (ie the move  a valid one) is not checked for and is assumed to be the case.
    '''
    chess_board = position.getchess_board()
    piece = chess_board[y][x][0]
    color = chess_board[y][x][1]
    player = position.get_player()
    castling_rights = position.getCastleRights()
    EnP_Target = position.getEnP()
    half_move_clock = position.getHMC()
    if is_occupied(chess_board, x2, y2) or piece == 'P':
        half_move_clock = 0
    else:
        half_move_clock += 1

    chess_board[y2][x2] = chess_board[y][x]
    chess_board[y][x] = 0


    if piece == 'K':

        castling_rights[player] = [False, False]
        if abs(x2 - x) == 2:
            if color == 'w':
                l = 7
            else:
                l = 0

            if x2 > x:
                chess_board[l][5] = 'R' + color
                chess_board[l][7] = 0
            else:
                chess_board[l][3] = 'R' + color
                chess_board[l][0] = 0

    if piece == 'R':
        if x == 0 and y == 0:
            castling_rights[1][1] = False
        elif x == 7 and y == 0:
            castling_rights[1][0] = False
        elif x == 0 and y == 7:
            castling_rights[0][1] = False
        elif x == 7 and y == 7:
            castling_rights[0][0] = False

    if piece == 'P':
        if EnP_Target == (x2, y2):
            if color == 'w':
                chess_board[y2 + 1][x2] = 0
            else:
                chess_board[y2 - 1][x2] = 0
        if abs(y2 - y) == 2:
            EnP_Target = (x, (y + y2) / 2)
        else:
            EnP_Target = -1

        if y2 == 0:
            chess_board[y2][x2] = 'Qw'
        elif y2 == 7:
            chess_board[y2][x2] = 'Qb'
    else:
        EnP_Target = -1

    player = 1 - player

    position.setplayer(player)
    position.setCastleRights(castling_rights)
    position.setEnP(EnP_Target)
    position.setHMC(half_move_clock)


def find_possible_squares(position, x, y, attack_search=False):
    '''
    This function takes as its input the current state of the chesschess_board, and a particular x and y coordinate.
    It will return for the piece on that chess_board a list of possible coordinates it could move to, including captures
    and excluding illegal moves (eg moves that leave a king under check). attack_search is an argument used to
    ensure infinite recursions do not occur.
    '''

    chess_board = position.getchess_board()
    player = position.get_player()
    castling_rights = position.getCastleRights()
    EnP_Target = position.getEnP()

    if len(chess_board[y][x]) != 2:
        return []
    piece = chess_board[y][x][0]
    color = chess_board[y][x][1]
    enemy_color = opp(color)
    list_of_tuples = []

    """
    *************************************************
    Branching over the types of pieces
    *************************************************
    """

    if piece == 'P':
        if color == 'w':
            if not is_occupied(chess_board, x, y - 1) and not attack_search:
                list_of_tuples.append((x, y - 1))

                if y == 6 and not is_occupied(chess_board, x, y - 2):
                    list_of_tuples.append((x, y - 2))

            if x != 0 and is_occupied_by(chess_board, x - 1, y - 1, 'black'):
                list_of_tuples.append((x - 1, y - 1))
            if x != 7 and is_occupied_by(chess_board, x + 1, y - 1, 'black'):
                list_of_tuples.append((x + 1, y - 1))
            if EnP_Target != -1:
                if EnP_Target == (x - 1, y - 1) or EnP_Target == (x + 1, y - 1):
                    list_of_tuples.append(EnP_Target)

        elif color == 'b':
            if not is_occupied(chess_board, x, y + 1) and not attack_search:
                list_of_tuples.append((x, y + 1))
                if y == 1 and not is_occupied(chess_board, x, y + 2):
                    list_of_tuples.append((x, y + 2))
            if x != 0 and is_occupied_by(chess_board, x - 1, y + 1, 'white'):
                list_of_tuples.append((x - 1, y + 1))
            if x != 7 and is_occupied_by(chess_board, x + 1, y + 1, 'white'):
                list_of_tuples.append((x + 1, y + 1))
            if EnP_Target == (x - 1, y + 1) or EnP_Target == (x + 1, y + 1):
                list_of_tuples.append(EnP_Target)

    elif piece == 'R':
        for i in [-1, 1]:
            kx = x
            while True:
                kx = kx + i
                if kx <= 7 and kx >= 0:

                    if not is_occupied(chess_board, kx, y):
                        list_of_tuples.append((kx, y))
                    else:
                        if is_occupied_by(chess_board, kx, y, enemy_color):
                            list_of_tuples.append((kx, y))
                        break
                else:
                    break

        for i in [-1, 1]:
            ky = y
            while True:
                ky = ky + i
                if ky <= 7 and ky >= 0:
                    if not is_occupied(chess_board, x, ky):
                        list_of_tuples.append((x, ky))
                    else:
                        if is_occupied_by(chess_board, x, ky, enemy_color):
                            list_of_tuples.append((x, ky))
                        break
                else:
                    break

    elif piece == 'N':
        for dx in [-2, -1, 1, 2]:
            if abs(dx) == 1:
                sy = 2
            else:
                sy = 1
            for dy in [-sy, +sy]:
                list_of_tuples.append((x + dx, y + dy))
        list_of_tuples = filter_by_color(chess_board, list_of_tuples, color)
    elif piece == 'B':
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                kx = x
                ky = y
                while True:
                    kx = kx + dx
                    ky = ky + dy
                    if kx <= 7 and kx >= 0 and ky <= 7 and ky >= 0:
                        if not is_occupied(chess_board, kx, ky):
                            list_of_tuples.append((kx, ky))
                        else:
                            if is_occupied_by(chess_board, kx, ky, enemy_color):
                                list_of_tuples.append((kx, ky))
                            break
                    else:
                        break

    elif piece == 'Q':
        chess_board[y][x] = 'R' + color
        list_rook = find_possible_squares(position, x, y, True)
        chess_board[y][x] = 'B' + color
        list_bishop = find_possible_squares(position, x, y, True)
        list_of_tuples = list_rook + list_bishop
        chess_board[y][x] = 'Q' + color
    elif piece == 'K':
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                list_of_tuples.append((x + dx, y + dy))
        list_of_tuples = filter_by_color(chess_board, list_of_tuples, color)
        if not attack_search:
            right = castling_rights[player]

            if (right[0] and
                    chess_board[y][7] != 0 and
                    chess_board[y][7][0] == 'R' and
                    not is_occupied(chess_board, x + 1, y) and
                    not is_occupied(chess_board, x + 2, y) and
                    not is_attacked_by(position, x, y, enemy_color) and
                    not is_attacked_by(position, x + 1, y, enemy_color) and
                    not is_attacked_by(position, x + 2, y, enemy_color)):
                list_of_tuples.append((x + 2, y))

            if (right[1] and
                    chess_board[y][0] != 0 and
                    chess_board[y][0][0] == 'R' and
                    not is_occupied(chess_board, x - 1, y) and
                    not is_occupied(chess_board, x - 2, y) and
                    not is_occupied(chess_board, x - 3, y) and
                    not is_attacked_by(position, x, y, enemy_color) and
                    not is_attacked_by(position, x - 1, y, enemy_color) and
                    not is_attacked_by(position, x - 2, y, enemy_color)):
                list_of_tuples.append((x - 2, y))
    """
    ******************* End of Pieces branching ********************
    """
    if not attack_search:
        new_list = []
        for tuple_q in list_of_tuples:
            x2 = int(tuple_q[0])
            y2 =int( tuple_q[1])
            temp_pos = position.clone()
            make_move(temp_pos, x, y, x2, y2)
            if not is_check(temp_pos, color):
                new_list.append(tuple_q)
        list_of_tuples = new_list
    return list_of_tuples
