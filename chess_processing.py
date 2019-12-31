'''
In this file, we are going to implement the chess board functions so they could be used by the main module.
El Koumy
31/12/2019
'''


def is_occupied(board,x,y):
    '''
    Returns true if a given coordinate on the board is not empty, and false otherwise.
    '''
    if board[y][x] == 0:
        return False
    return True


def is_occupied_by(board,x,y,color):
    '''
    Only returns true if the square specified by the coordinates is of the specific color inputted.
    '''
    if board[y][x]==0:
        return False
    if board[y][x][1] == color[0]:
        return True
    return False


def filter_by_color(board,list_of_tuples,color):
    '''
    This function takes the board state, a list of coordinates, and a color as input. It will return the same list,
    but without coordinates that are out of bounds of the board and also without those occupied by the pieces of the
    particular color passed to this function as an argument. In other words, if 'white' is passed in, it will not
    return any white occupied square.
    '''
    filtered_list = []
    for pos in list_of_tuples:
        x = pos[0]
        y = pos[1]
        if x>=0 and x<=7 and y>=0 and y<=7 and not is_occupied_by(board,x,y,color):
            #coordinates are on-board and no same-color piece is on the square.
            filtered_list.append(pos)
    return filtered_list



def look_for(board,piece):
    '''
    This functions takes the 2D array that represents a board and finds the indices of all the locations that is
    occupied by the specified piece. The list of indices is returned.
    '''
    list_of_locations = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == piece:
                x = col
                y = row
                list_of_locations.append((x,y))
    return list_of_locations


