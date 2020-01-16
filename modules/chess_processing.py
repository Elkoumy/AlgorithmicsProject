def is_occupied_by(chess_board, x, y, square_color):
    """

    Args:
        chess_board:
        x: x-axis coordinate
        y: y-axis coordinate
        square_color: square color

    Returns:
        is_occupied_by function returns true or false based on the color of the square.
    """

    if chess_board[int(y)][int(x)] == 0:
        return False
    if chess_board[y][x][1] == square_color[0]:
        return True
    return False


def filter_by_color(chess_board, input_list, player_color):
    """

    Args:
        chess_board: 2d array of the board state
        input_list: the same list as the input list
        player_color: white or black

    Returns:
        this function return the filtered list of pieces based on the color.

    """

    filtered = []
    for i in input_list:
        x = i[0]
        y = i[1]
        if x >= 0 and x <= 7 and y >= 0 and y <= 7 and not is_occupied_by(chess_board, x, y, player_color):
            filtered.append(i)
    return filtered


def is_occupied(chess_board, x, y):
    """
    Args:
        chess_board:
        x: x-axis coordinate
        y: y-axis coordinate

    Returns:
        is_occupied function returns true if the input coordinate is not empty, and false on the other hand.
    """

    if chess_board[int(y)][int(x)] == 0:
        return False
    return True


def look_for(chess_board, piece):
    """
    Args:
        chess_board: 2d array of the board state
        piece: any piece on the board.

    Returns: this function returns list of indices w.r.t a specific piece

    """

    positions = []
    for row in range(8):
        for col in range(8):
            if chess_board[row][col] == piece:
                x = col
                y = row
                positions.append((x, y))
    return positions


def opp(color):
    """

    Args:
        color: white or black

    Returns:
        this function returns the inverse color of the opponent

    """

    color = color[0]
    if color == 'w':
        oppcolor = 'b'
    else:
        oppcolor = 'w'
    return oppcolor


def is_attacked_by(position, target_x, target_y, color):
    """

    Args:
        position: position of the piece
        target_x: x-coordinate
        target_y: y-coordinate
        color: color of the piece

    Returns: this function returns a list of squares which are being attacked by any set of pieces.

    """

    chess_board = position.getchess_board()
    color = color[0]
    list_of_attacked_squares = []
    for x in range(8):
        for y in range(8):
            if chess_board[y][x] != 0:

                if chess_board[y][x][1] == color:
                    list_of_attacked_squares.extend(
                        find_possible_squares(position, x, y, True))

    return (target_x, target_y) in list_of_attacked_squares


def is_check(position, color):
    """

    Args:
        position: position to test attack
        color: white or black

    Returns: this function returns true if the king under attack of a specific piece

    """

    chess_board = position.getchess_board()
    color = color[0]
    enemy = opp(color)
    piece = 'K' + color
    x, y = look_for(chess_board, piece)[0]
    return is_attacked_by(position, x, y, enemy)


def is_check_mate(position, color=-1):
    """

    Args:
        position: piece position
        color: white or black

    Returns: this function returns true of the check mate, false otherwise.

    """

    if color == -1:
        return is_check_mate(position, 'white') or is_check_mate(position, 'b')
    color = color[0]
    if is_check(position, color) and all_moves(position, color) == []:
        return True
    return False


def is_stalemate(position):
    """

    Args:
        position: piece position

    Returns: this function returns true if the specified position is a stalemate, false otherwise

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

    Args:
        position: piece position
        color: white or black

    Returns: this function returns all possible positions based on a specific color.

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

    Args:
        position:  piece position
        color: white or black side

    Returns: this function returns all possible moves based on the current position and the current color

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

    Args:
        position: position of the piece

    Returns: this function returns a unique key based on the position of the piece.

    """

    chess_board = position.getchess_board()
    chess_board_tuple = []
    for row in chess_board:
        chess_board_tuple.append(tuple(row))
    chess_board_tuple = tuple(chess_board_tuple)
    rights = position.get_castle_rights()
    tuple_rights = (tuple(rights[0]), tuple(rights[1]))
    key = (chess_board_tuple, position.get_player(),
           tuple_rights)
    return key


def make_move(position, x, y, x2, y2):
    """
    this function used to make the actual move on the board
    Args:
        position:
        x: x-axis of the source
        y: y-axix of the source
        x2: x-axis of the destination
        y2: y-axis of the destination

    Returns:

    """

    chess_board = position.getchess_board()
    piece = chess_board[y][x][0]
    color = chess_board[y][x][1]
    player = position.get_player()
    castling_rights = position.get_castle_rights()
    square_target = position.get_square_target()
    half_move_clock = position.get_half_move_clock()
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
        if square_target == (x2, y2):
            if color == 'w':
                chess_board[y2 + 1][x2] = 0
            else:
                chess_board[y2 - 1][x2] = 0
        if abs(y2 - y) == 2:
            square_target = (x, (y + y2) / 2)
        else:
            square_target = -1

        if y2 == 0:
            chess_board[y2][x2] = 'Qw'
        elif y2 == 7:
            chess_board[y2][x2] = 'Qb'
    else:
        square_target = -1

    player = 1 - player

    position.set_player(player)
    position.set_castle_rights(castling_rights)
    position.set_square_target(square_target)
    position.set_half_move_clock(half_move_clock)


def find_possible_squares(position, x, y, attack_search=False):
    """

    Args:
        position: piece position
        x: x-axis
        y: y-axis
        attack_search: avoid unlimited recursion

    Returns: this function returns a list of possible moves based on a specific position

    """

    chess_board = position.getchess_board()
    player = position.get_player()
    castling_rights = position.get_castle_rights()
    square_target = position.get_square_target()

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
            if square_target != -1:
                if square_target == (x - 1, y - 1) or square_target == (x + 1, y - 1):
                    list_of_tuples.append(square_target)

        elif color == 'b':
            if not is_occupied(chess_board, x, y + 1) and not attack_search:
                list_of_tuples.append((x, y + 1))
                if y == 1 and not is_occupied(chess_board, x, y + 2):
                    list_of_tuples.append((x, y + 2))
            if x != 0 and is_occupied_by(chess_board, x - 1, y + 1, 'white'):
                list_of_tuples.append((x - 1, y + 1))
            if x != 7 and is_occupied_by(chess_board, x + 1, y + 1, 'white'):
                list_of_tuples.append((x + 1, y + 1))
            if square_target == (x - 1, y + 1) or square_target == (x + 1, y + 1):
                list_of_tuples.append(square_target)

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
            y2 = int(tuple_q[1])
            temp_pos = position.clone()
            make_move(temp_pos, x, y, x2, y2)
            if not is_check(temp_pos, color):
                new_list.append(tuple_q)
        list_of_tuples = new_list
    return list_of_tuples
