# game lib python
import pygame
from pygame.locals import *
import pickle
import threading
import os
from modules.chess_ai import *

##############################################################
###################### GUI ##################################
#############################################################
def coordinate_to_pixel(chess_coord):
    """

    Args:
        chess_coord: x, and y axis

    Returns: this function returns the pixel values for any x,y coordinates.

    """
    x,y = chess_coord
    if is_ai:
        if ai_player==0:
            return ((7-x)*square_width, (7-y)*square_height)
        else:
            return (x*square_width, y*square_height)

def pixel_to_coordinate(pixel_coord):
    """

    Args:
        pixel_coord: pixel values for any square

    Returns: this function returns x,y coordinates

    """
    x,y = pixel_coord[0]/square_width, pixel_coord[1]/square_height

    if is_ai:
        if ai_player==0:
            return (7-x,7-y)
        else:
            return (x,y)

def get_piece(chess_coord):
    """
    Args:
        chess_coord: state of the board

    Returns:

    """
    for piece in list_of_white_pieces+list_of_black_pieces:
        if piece.get_info()[0] == chess_coord:
            return piece


def generate_piece(chess_board):
    """

    Args:
        chess_board: state of the board

    Returns: this function returns a list of white and black pieces.

    """
    list_of_white_pieces = []
    list_of_black_pieces = []
    for i in range(8):
        for k in range(8):
            if chess_board[i][k]!=0:
                p = pieceDisplay(chess_board[i][k],(k,i),square_width,square_height)
                if chess_board[i][k][1]=='w':
                    list_of_white_pieces.append(p)
                else:
                    list_of_black_pieces.append(p)
    return [list_of_white_pieces,list_of_black_pieces]

def create_piece_display(list_of_tuples):
    """

    Args:
        list_of_tuples: tuples of pices square

    Returns: this function shade list of tuples

    """
    global list_of_shades
    list_of_shades = []
    if is_transition:
        return
    if is_draw:

        coord = look_for(chess_board,'Kw')[0]
        shade = imageDispaly(circle_image_yellow,coord)
        list_of_shades.append(shade)
        coord = look_for(chess_board,'Kb')[0]
        shade = imageDispaly(circle_image_yellow,coord)
        list_of_shades.append(shade)
        return

    if end_game:
        coord = look_for(chess_board,'K'+winner)[0]
        shade = imageDispaly(circle_image_green_big,coord)
        list_of_shades.append(shade)

    if is_check(position,'white'):
        coord = look_for(chess_board,'Kw')[0]
        shade = imageDispaly(circle_image_red,coord)
        list_of_shades.append(shade)

    if is_check(position,'black'):
        coord = look_for(chess_board,'Kb')[0]
        shade = imageDispaly(circle_image_red,coord)
        list_of_shades.append(shade)

    for pos in list_of_tuples:
        if is_occupied(chess_board,pos[0],pos[1]):
            img = circle_image_capture
        else:
            img = circle_image_green
        shade = imageDispaly(img,pos)
        list_of_shades.append(shade)

def plot_chess_game():
    #create background
    screen.blit(background,(0,0))
    # who is should play
    if player==1:
        order = [list_of_white_pieces,list_of_black_pieces]
    else:
        order = [list_of_black_pieces,list_of_white_pieces]
    if is_transition:

        order = list(reversed(order))

    if is_draw or end_game or is_aiThink:
        #pieceDisplay
        for shade in list_of_shades:
            img,chess_coord = shade.get_info()
            pixel_coord = coordinate_to_pixel(chess_coord)
            screen.blit(img,pixel_coord)
    if prev_move[0]!=-1 and not is_transition:
        x,y,x2,y2 = prev_move
        screen.blit(yellowbox_image,coordinate_to_pixel((x,y)))
        screen.blit(yellowbox_image,coordinate_to_pixel((x2,y2)))

    for piece in order[0]:

        chess_coord,subsection,pos = piece.get_info()
        pixel_coord = coordinate_to_pixel(chess_coord)
        if pos==(-1,-1):
            screen.blit(pieces_image,pixel_coord,subsection)
        else:
            screen.blit(pieces_image,pos,subsection)
    if not (is_draw or end_game or is_aiThink):
        for shade in list_of_shades:
            img,chess_coord = shade.get_info()
            pixel_coord = coordinate_to_pixel(chess_coord)
            screen.blit(img,pixel_coord)
    for piece in order[1]:
        chess_coord,subsection,pos = piece.get_info()
        pixel_coord = coordinate_to_pixel(chess_coord)
        if pos==(-1,-1):
            screen.blit(pieces_image,pixel_coord,subsection)
        else:
            screen.blit(pieces_image,pos,subsection)


#******************************************************************#
#******************    Start Main    ******************************
#******************************************************************#

# chess game init
chess_board = [ ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],#8
          ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],      #7
          [0,    0,    0,    0,    0,    0,    0,    0],         #6
          [0,    0,    0,    0,    0,    0,    0,    0],         #5
          [0,    0,    0,    0,    0,    0,    0,    0],         #4
          [0,    0,    0,    0,    0,    0,    0,    0],         #3
          ['Pw', 'Pw', 'Pw',  'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],     #2
          ['Rw', 'Nw', 'Bw',  'Qw', 'Kw', 'Bw', 'Nw', 'Rw'] ]    #1
           # a      b     c     d     e     f     g     h


# next move 0 for white, 1 for black
player = 0
castling_rights = [[True, True],[True, True]]
En_Passant_Target = -1
half_move_clock = 0
position = chessPosition(chess_board, player, castling_rights, En_Passant_Target, half_move_clock)
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

#init pygame
pygame.init()
#Load the screen with any arbitrary size for now:
screen = pygame.display.set_mode((500,500))

# images for chess_board.
background = pygame.image.load(os.path.join('Images_GUI', 'board.png')).convert()
pieces_image = pygame.image.load(os.path.join('Images_GUI', 'Chess_Pieces_Sprite.png')).convert_alpha()
circle_image_green = pygame.image.load(os.path.join('Images_GUI', 'green_circle_small.png')).convert_alpha()
circle_image_capture = pygame.image.load(os.path.join('Images_GUI', 'green_circle_neg.png')).convert_alpha()
circle_image_red = pygame.image.load(os.path.join('Images_GUI', 'red_circle_big.png')).convert_alpha()
greenbox_image = pygame.image.load(os.path.join('Images_GUI', 'green_box.png')).convert_alpha()
circle_image_yellow = pygame.image.load(os.path.join('Images_GUI', 'yellow_circle_big.png')).convert_alpha()
circle_image_green_big = pygame.image.load(os.path.join('Images_GUI', 'green_circle_big.png')).convert_alpha()
yellowbox_image = pygame.image.load(os.path.join('Images_GUI', 'yellow_box.png')).convert_alpha()
playwhite_pic = pygame.image.load(os.path.join('Images_GUI', 'start.png')).convert_alpha()
size_of_bg = background.get_rect().size
square_width =int( size_of_bg[0]/8)
square_height = int(size_of_bg[1]/8)



pieces_image = pygame.transform.scale(pieces_image,
                                      (square_width*6,square_height*2))
circle_image_green = pygame.transform.scale(circle_image_green,
                                      (square_width, square_height))
circle_image_capture = pygame.transform.scale(circle_image_capture,
                                      (square_width, square_height))
circle_image_red = pygame.transform.scale(circle_image_red,
                                      (square_width, square_height))
greenbox_image = pygame.transform.scale(greenbox_image,
                                      (square_width, square_height))
yellowbox_image = pygame.transform.scale(yellowbox_image,
                                      (square_width, square_height))
circle_image_yellow = pygame.transform.scale(circle_image_yellow,
                                             (square_width, square_height))
circle_image_green_big = pygame.transform.scale(circle_image_green_big,
                                             (square_width, square_height))

playwhite_pic = pygame.transform.scale(playwhite_pic,
                                      (square_width*4,square_height*4))


screen = pygame.display.set_mode(size_of_bg)
pygame.display.set_caption('Chess AI')
screen.blit(background,(0,0))


list_of_white_pieces,list_of_black_pieces = generate_piece(chess_board)

list_of_shades = []

clock = pygame.time.Clock()
is_down = False
is_clicked = False
is_transition = False
is_draw = False
end_game = False
is_record = False

is_aiThink = False
openings = defaultdict(list)

try:
    file_handle = open('openingTable.txt', 'r+')
    openings = pickle.loads(file_handle.read())
except:
    if is_record:
        file_handle = open('openingTable.txt', 'w')

# hold nodes that have been evaluated
searched = {}
prev_move = [-1,-1,-1,-1]
ax,ay=0,0
numm = 0
is_menu = True
is_ai = True
is_flip = -1
ai_player = -1
game_ended = False


#***********************************************************#
#****************** infinite loop for the game **************
#***********************************************************#

while not game_ended:

    if is_menu:
        screen.blit(background,(0,0))
        if is_ai==True:
            screen.blit(playwhite_pic,(square_width*2,square_height*2))
        if is_flip!=-1:
            plot_chess_game()
            is_menu = False
            if is_ai and ai_player==0:
                color_sign=1
                best_move_return = []
                move_thread = threading.Thread(target=negamax,
                            args = (position,6,-1000000,1000000,color_sign,best_move_return))
                move_thread.start()
                is_aiThink = True
            continue
        for event in pygame.event.get():
            if event.type==QUIT:
                game_ended = True
                break
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                ai_player = 1
                is_flip = False
                is_ai = True
        pygame.display.update()
        continue

    numm+=1
    if is_aiThink and numm%6==0:
        ax+=1
        if ax==8:
            ay+=1
            ax=0
        if ay==8:
            ax,ay=0,0
        if ax%4==0:
            create_piece_display([])
        if ai_player==0:
            list_of_shades.append(imageDispaly(greenbox_image,(7-ax,7-ay)))
        else:
            list_of_shades.append(imageDispaly(greenbox_image,(ax,ay)))

    for event in pygame.event.get():

        if event.type==QUIT:
            game_ended = True

            break
        if end_game or is_transition or is_aiThink:
            continue
        if not is_down and event.type == MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            chess_coord = pixel_to_coordinate(pos)
            chess_coord=(int(chess_coord[0]),int(chess_coord[1]))

            x =chess_coord[0]
            y = chess_coord[1]

            if not is_occupied_by(chess_board,x,y,'wb'[player]):
                continue

            drag_piece = get_piece(chess_coord)
            print(drag_piece)
            list_of_tuples = find_possible_squares(position,x,y)

            create_piece_display(list_of_tuples)

            if ((drag_piece.pieceDisplayinfo[0]=='K') and
                (is_check(position,'white') or is_check(position,'black'))):
                None
            else:
                list_of_shades.append(imageDispaly(greenbox_image,(x,y)))
            is_down = True
        if (is_down or is_clicked) and event.type == MOUSEBUTTONUP:
            is_down = False
            drag_piece.set_pos((-1,-1))
            pos = pygame.mouse.get_pos()
            chess_coord = pixel_to_coordinate(pos)
            chess_coord = (int(chess_coord[0]), int(chess_coord[1]))
            x2 = chess_coord[0]
            y2 = chess_coord[1]

            is_transition = False
            if (x,y)==(x2,y2):

                if not is_clicked:

                    is_clicked = True
                    prevPos = (x,y)
                else:

                    x,y = prevPos
                    if (x,y)==(x2,y2):

                        is_clicked = False

                        create_piece_display([])
                    else:
                        if is_occupied_by(chess_board,x2,y2,'wb'[player]):

                            is_clicked = True
                            prevPos = (x2,y2)
                        else:
                            is_clicked = False
                            create_piece_display([])
                            is_transition = True


            if not (x2,y2) in list_of_tuples:
                is_transition = False
                continue

            if is_record:
                key = pos_to_key(position)
                if [(x,y),(x2,y2)] not in openings[key]:
                    openings[key].append([(x,y),(x2,y2)])

            make_move(position,x,y,x2,y2)
            prev_move = [x,y,x2,y2]

            player = position.get_player()
            position.add_to_history(position)

            half_move_clock = position.get_half_move_clock()
            if half_move_clock>=100 or is_stalemate(position) or position.check_repetition():
                is_draw = True
                end_game = True

            if is_check_mate(position,'white'):
                winner = 'b'
                end_game = True
            if is_check_mate(position,'black'):
                winner = 'w'
                end_game = True

            if is_ai and not end_game:
                if player==0:
                    color_sign = 1
                else:
                    color_sign = -1
                best_move_return = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,3,-1000000,1000000,color_sign,best_move_return))
                move_thread.start()
                is_aiThink = True
            drag_piece.set_coord((x2,y2))
            if not is_transition:
                list_of_white_pieces,list_of_black_pieces = generate_piece(chess_board)
            else:
                moving_piece = drag_piece
                origin = coordinate_to_pixel((x,y))
                destiny = coordinate_to_pixel((x2,y2))
                moving_piece.set_pos(origin)
                step = (destiny[0]-origin[0],destiny[1]-origin[1])

            create_piece_display([])
    if is_transition:
        p,q = moving_piece.get_pos()
        dx2,dy2 = destiny
        n= 30.0
        if abs(p-dx2)<=abs(step[0]/n) and abs(q-dy2)<=abs(step[1]/n):
            moving_piece.set_pos((-1,-1))
            list_of_white_pieces,list_of_black_pieces = generate_piece(chess_board)
            is_transition = False
            create_piece_display([])
        else:
            moving_piece.set_pos((p+step[0]/n,q+step[1]/n))
    if is_down:
        m,k = pygame.mouse.get_pos()
        drag_piece.set_pos((m-square_width/2,k-square_height/2))

    if is_aiThink and not is_transition:
        if not move_thread.isAlive():

            is_aiThink = False
            create_piece_display([])
            print(f"best_move_return: {best_move_return}")
            p1, p2 = best_move_return
            x,y = p1
            x2,y2 = p2
            make_move(position,x,y,x2,y2)
            prev_move = [x,y,x2,y2]
            player = position.get_player()
            half_move_clock = position.get_half_move_clock()
            position.add_to_history(position)
            if half_move_clock>=100 or is_stalemate(position) or position.check_repetition():
                is_draw = True
                end_game = True
            if is_check_mate(position,'white'):
                winner = 'b'
                end_game = True
            if is_check_mate(position,'black'):
                winner = 'w'
                end_game = True
            is_transition = True
            moving_piece = get_piece((x,y))
            origin = coordinate_to_pixel((x,y))
            destiny = coordinate_to_pixel((x2,y2))
            moving_piece.set_pos(origin)
            step = (destiny[0]-origin[0],destiny[1]-origin[1])

    plot_chess_game()
    pygame.display.update()


    clock.tick(60)


pygame.quit()
if is_record:
    file_handle.seek(0)
    pickle.dump(openings,file_handle)
    file_handle.truncate()
    file_handle.close()
